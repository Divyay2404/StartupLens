import logging
from typing import Dict, Any, List, Optional
import httpx
from app.config import settings
from app.models.schemas import (
    IdeaInputRequest, OpportunityReport, ResearchPlan,
    TrendSignal, ScholarFinding, PatentSignal
)
from app.services.query_planner import QueryPlanner
from app.services.serpapi_client import SerpApiClient
from app.services.evidence_engine import EvidenceEngine
from app.services.competitor_engine import CompetitorEngine
from app.services.opportunity_engine import OpportunityEngine

logger = logging.getLogger(__name__)

class AIEngine:
    """
    Main orchestration engine connecting Idea -> QueryPlanner -> SerpApi Multi-Engine ->
    Evidence Engine -> Competitor Engine -> Opportunity Gap Engine -> Opportunity Report.
    """

    @staticmethod
    async def analyze_idea(request: IdeaInputRequest) -> OpportunityReport:
        idea = request.idea.strip()
        region = request.target_region or "Global"
        include_patents = request.include_patents
        
        # 1. Step 1: AI Query Planner
        research_plan: ResearchPlan = QueryPlanner.plan(
            idea=idea,
            target_region=region,
            include_patents=include_patents
        )

        # 2. Step 2: SerpApi Multi-Engine live search
        serpapi_client = SerpApiClient(api_key=request.serpapi_api_key or settings.SERPAPI_API_KEY)
        raw_evidence = await serpapi_client.execute_multi_engine_research(idea, research_plan.queries)

        # 3. Step 3: Evidence Engine (Normalize, Deduplicate, Rank)
        query_words = [q.query for q in research_plan.queries]
        processed_evidence = EvidenceEngine.process_and_rank(raw_evidence, query_words)
        evidence_items = processed_evidence["evidence_items"]

        # 4. Step 4: Competitor Engine (Extract Competitors & Killer Feature Matrix)
        competitor_analysis = CompetitorEngine.extract_competitors_and_matrix(
            idea=idea,
            evidence_items=evidence_items,
            domain=research_plan.core_domain
        )
        competitors = competitor_analysis["competitors"]
        matrix = competitor_analysis["matrix"]

        # 5. Extract Trend, Scholar, News, Patent objects
        trend_raw = raw_evidence.get("google_trends", {})
        trend_signals: List[TrendSignal] = []
        if trend_raw and isinstance(trend_raw, dict):
            trend_signals.append(TrendSignal(
                keyword=trend_raw.get("keyword", idea),
                timeline=trend_raw.get("timeline", []),
                direction=trend_raw.get("direction", "Rising"),
                growth_rate=trend_raw.get("growth_rate", "+45%"),
                related_queries=trend_raw.get("related_queries", []),
                related_topics=trend_raw.get("related_topics", [])
            ))

        scholar_insights: List[ScholarFinding] = []
        for s in raw_evidence.get("google_scholar", [])[:3]:
            scholar_insights.append(ScholarFinding(
                title=s.get("title", ""),
                link=s.get("link", ""),
                authors=s.get("authors", "Academic Authors"),
                year=s.get("year", "Recent"),
                citations=s.get("citations", 0),
                key_takeaway=s.get("snippet", "")
            ))

        patents: List[PatentSignal] = []
        if include_patents:
            for p in raw_evidence.get("google_patents", [])[:3]:
                patents.append(PatentSignal(
                    patent_id=p.get("patent_id", "US-PAT"),
                    title=p.get("title", ""),
                    assignee=p.get("assignee", "Patent Assignee"),
                    filing_date=p.get("filing_date", "Recent"),
                    summary=p.get("snippet", ""),
                    link=p.get("link", "")
                ))

        news_developments = raw_evidence.get("google_news", [])[:4]

        # 6. Step 5: Opportunity Gap Engine (Synthesizes Gaps, Viability, and Roadmap)
        opportunity_synthesis = OpportunityEngine.synthesize_opportunity(
            idea=idea,
            research_plan=research_plan,
            competitors=competitors,
            matrix=matrix,
            trend_signals=trend_signals,
            scholar_insights=scholar_insights,
            patents=patents,
            news_items=news_developments
        )

        return OpportunityReport(
            idea=idea,
            research_plan=research_plan,
            executive_summary=opportunity_synthesis["executive_summary"],
            core_opportunity=opportunity_synthesis["core_opportunity"],
            viability=opportunity_synthesis["viability"],
            competitor_matrix=matrix,
            competitors=competitors,
            gaps=opportunity_synthesis["gaps"],
            trend_signals=trend_signals,
            scholar_insights=scholar_insights,
            news_developments=news_developments,
            patents=patents,
            strategic_roadmap=opportunity_synthesis["roadmap"],
            meta={
                "is_live_serpapi": raw_evidence.get("is_live_serpapi", False),
                "engines_queried": raw_evidence.get("engines_queried", []),
                "total_evidence_sources": len(evidence_items),
                "disclaimer": "Patent results are exploratory intelligence signals, not legal clearance or freedom-to-operate advice. Opportunity assessments do not guarantee commercial success."
            }
        )
