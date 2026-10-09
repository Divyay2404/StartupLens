from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class IdeaInputRequest(BaseModel):
    idea: str = Field(..., min_length=3, description="The startup or project idea description")
    target_region: Optional[str] = Field("Global", description="Target region or market")
    include_patents: bool = Field(True, description="Whether to include Google Patents analysis")
    serpapi_api_key: Optional[str] = Field(None, description="Optional custom SerpApi key")
    ai_api_key: Optional[str] = Field(None, description="Optional custom Gemini or OpenAI key")

class TargetQuery(BaseModel):
    engine: str
    query: str
    purpose: str

class ResearchPlan(BaseModel):
    summary: str
    core_domain: str
    target_users: str
    queries: List[TargetQuery]

class SearchEvidenceItem(BaseModel):
    title: str
    link: str
    snippet: str
    source: str
    engine: str
    extra: Dict[str, Any] = {}

class CompetitorItem(BaseModel):
    name: str
    url: Optional[str] = ""
    summary: str
    target_audience: str
    pricing_model: Optional[str] = "Subscription / Freemium"
    strengths: List[str] = []
    weaknesses: List[str] = []
    features: Dict[str, str] = {}  # e.g., {"Offline First": "no", "Low Cost": "partial"}

class MatrixFeatureRow(BaseModel):
    feature_name: str
    category: str = "Core Capability"
    importance: str = "High"  # "Critical", "High", "Medium"
    competitor_ratings: Dict[str, str] = {}  # "yes" (✓), "no" (✗), "partial" (■)
    user_idea_rating: str = "yes"  # "yes" (✓)
    opportunity_reason: str

class OpportunityGap(BaseModel):
    title: str
    gap_type: str  # "Technical", "Market Accessibility", "Pricing & Distribution", "UX & Simplicity"
    description: str
    evidence_sources: List[str] = []
    recommended_differentiation: str

class TrendSignal(BaseModel):
    keyword: str
    timeline: List[Dict[str, Any]] = []
    direction: str = "Rising"
    growth_rate: str = "+35%"
    related_queries: List[str] = []
    related_topics: List[str] = []

class ScholarFinding(BaseModel):
    title: str
    link: Optional[str] = ""
    authors: str = "Unknown"
    year: Optional[str] = "Recent"
    citations: Optional[int] = 0
    key_takeaway: str

class PatentSignal(BaseModel):
    patent_id: str
    title: str
    assignee: str
    filing_date: Optional[str] = ""
    summary: str
    link: Optional[str] = ""

class ViabilityScore(BaseModel):
    overall: int  # 0 - 100
    market_demand: int  # 0 - 100
    competitor_saturation: int  # 0 - 100 (lower means less crowded)
    differentiation_potential: int  # 0 - 100
    tech_feasibility: int  # 0 - 100
    verdict: str
    rationale: str

class RoadmapStep(BaseModel):
    phase: str
    title: str
    focus: str
    deliverables: List[str]

class OpportunityReport(BaseModel):
    idea: str
    research_plan: ResearchPlan
    executive_summary: str
    core_opportunity: str
    viability: ViabilityScore
    competitor_matrix: List[MatrixFeatureRow]
    competitors: List[CompetitorItem]
    gaps: List[OpportunityGap]
    trend_signals: List[TrendSignal]
    scholar_insights: List[ScholarFinding]
    news_developments: List[Dict[str, Any]]
    patents: List[PatentSignal]
    strategic_roadmap: List[RoadmapStep]
    meta: Dict[str, Any]
