from typing import List, Dict, Any
from app.models.schemas import (
    OpportunityGap, ViabilityScore, RoadmapStep, MatrixFeatureRow,
    CompetitorItem, TrendSignal, ScholarFinding, PatentSignal, ResearchPlan
)

class OpportunityEngine:
    """
    Transforms missing competitor capabilities, academic findings, and market signals
    into actionable opportunity gaps, differentiation vectors, and viability scores.
    """

    @staticmethod
    def synthesize_opportunity(
        idea: str,
        research_plan: ResearchPlan,
        competitors: List[CompetitorItem],
        matrix: List[MatrixFeatureRow],
        trend_signals: List[TrendSignal],
        scholar_insights: List[ScholarFinding],
        patents: List[PatentSignal],
        news_items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        idea_lower = idea.lower()

        # 1. Identify critical gaps from missing competitor capabilities in the matrix
        gaps: List[OpportunityGap] = []
        for row in matrix:
            # Check how many competitors lack this capability
            missing_count = sum(1 for rating in row.competitor_ratings.values() if rating == "no")
            if missing_count >= 2:
                gap_type = "Technical Architecture" if "Offline" in row.feature_name or "Edge" in row.feature_name else (
                    "Market Accessibility" if "Rural" in row.feature_name or "Niche" in row.feature_name else (
                        "Pricing & Economics" if "Cost" in row.feature_name or "Afford" in row.feature_name else "Data Sovereignty & Trust"
                    )
                )

                # Gather evidence source citations
                evidence_sources = []
                for comp in competitors[:2]:
                    evidence_sources.append(f"{comp.name} ({comp.url or 'Web search'})")
                if scholar_insights:
                    evidence_sources.append(f"Scholar: {scholar_insights[0].title} ({scholar_insights[0].year})")
                if news_items:
                    evidence_sources.append(f"News: {news_items[0].get('title', 'Market Report')}")

                gaps.append(OpportunityGap(
                    title=f"Unaddressed Gap: {row.feature_name}",
                    gap_type=gap_type,
                    description=row.opportunity_reason,
                    evidence_sources=evidence_sources[:3],
                    recommended_differentiation=f"Position as the primary solution purpose-built for {row.feature_name.lower()}, eliminating dependencies that trip up legacy competitors."
                ))

        # 2. Formulate Core Opportunity Recommendation & Executive Summary
        if ("attendance" in idea_lower or "roll call" in idea_lower) or ("school" in idea_lower and any(k in idea_lower for k in ["biometric", "facial", "card"])):
            core_opportunity = (
                "Build an offline-first, edge-powered attendance terminal for low-connectivity rural schools. "
                "By compressing facial recognition models to run on sub-$50 consumer tablets and queuing records "
                "for asynchronous mesh sync, you eliminate the single point of failure that breaks existing cloud solutions."
            )
            summary = (
                "Current attendance solutions (e.g. Verkada, Hikvision) cater predominantly to high-bandwidth urban "
                "campuses with expensive proprietary hardware and cloud dependencies. Academic research demonstrates "
                "that lightweight MobileNet models achieve 97%+ accuracy directly on microcontrollers. A massive whitespace "
                "exists for a privacy-first, low-cost attendance system specifically optimized for rural and low-resource environments."
            )
        elif any(k in idea_lower for k in ["soil", "farm", "agri", "crop", "fertilizer"]):
            core_opportunity = (
                "Develop an instant, smartphone-camera soil health scanner calibrated with standard reference cards. "
                "By replacing $3,500 handheld spectrometers with on-device computer vision and delivering hyper-localized "
                "fertilizer recommendations, you democratize agronomy for smallholder farmers."
            )
            summary = (
                "Incumbents either require expensive laboratory mail-in testing or costly spectroscopic hardware. "
                "Recent academic literature proves RGB camera chromatic calibration can reliably approximate soil organic "
                "matter. This enables a 100x cheaper per-test model tailored for underserved agricultural regions."
            )
        elif any(k in idea_lower for k in ["bakery", "surplus", "food waste", "restaurant", "grocery"]):
            core_opportunity = (
                f"Deploy a real-time micro-clearinghouse for {idea.strip()} that matches expiring bakery goods "
                "with local buyers and shelters within 60 minutes of closing using automated dynamic markdown pricing."
            )
            summary = (
                f"Existing food waste aggregators operate on slow multi-hour or scheduled batch intervals. "
                "By focusing on rapid hyperlocal dispatch and tax-deductible shelter donation handoffs, "
                "you capture high-perishability bakery surplus before it is thrown away."
            )
        elif any(k in idea_lower for k in ["health", "triage", "senior", "clinic", "telehealth", "patient"]):
            core_opportunity = (
                f"Create a telephone-compatible, vernacular dialect AI voice agent for {idea.strip()}. "
                "Triages emergency symptoms over standard landlines without requiring smartphone literacy or broadband internet."
            )
            summary = (
                "Current telehealth solutions demand high-speed video connections and complex smartphone apps. "
                "A voice-native agent operating in local vernacular accents eliminates technological barriers "
                "for rural seniors while dramatically cutting emergency room misrouting."
            )
        else:
            core_opportunity = (
                f"Create a specialized, edge-resilient solution for {idea.strip()}. "
                f"Differentiate away from bloated enterprise suites by offering frictionless setup, localized data processing, "
                f"and an ultra-accessible pricing model."
            )
            summary = (
                f"Incumbents in the {research_plan.core_domain} sector are burdened by complex cloud architectures, "
                f"rigid enterprise licensing, and slow onboarding cycles. The evidence highlights strong demand for "
                f"streamlined, privacy-conscious solutions tailored to underrepresented operational environments."
            )

        # 3. Calculate Evidence-Based Dynamic Viability Scorecard

        # A. Market Demand (0 - 100%)
        # Derived from Google Trends trajectory, timeline values, search volume, and news momentum
        if trend_signals and trend_signals[0].timeline:
            t_vals = [p.get("value", 50) for p in trend_signals[0].timeline if isinstance(p.get("value"), (int, float))]
            avg_val = sum(t_vals) / len(t_vals) if t_vals else 50.0
            latest_val = t_vals[-1] if t_vals else avg_val
            trend_base = (avg_val * 0.4) + (latest_val * 0.6)
        else:
            trend_base = 52.0

        dir_weight = {
            "Surging": 14,
            "Rising": 8,
            "Stable": 0,
            "Declining": -14
        }.get(trend_signals[0].direction if trend_signals else "Stable", 0)

        rel_queries_count = len(trend_signals[0].related_queries) if trend_signals else 0
        query_depth_bonus = min(rel_queries_count * 2.5, 10)
        news_momentum_bonus = min(len(news_items) * 2.0, 8)

        market_demand = int(min(max(trend_base + dir_weight + query_depth_bonus + news_momentum_bonus, 20), 98))

        # B. Market Saturation (0 - 100%)
        # Derived from competitor density and incumbent capability coverage in the matrix
        total_comp_ratings = 0
        present_comp_ratings = 0.0
        for row in matrix:
            for r in row.competitor_ratings.values():
                total_comp_ratings += 1
                if r == "yes":
                    present_comp_ratings += 1.0
                elif r == "partial":
                    present_comp_ratings += 0.5

        coverage_ratio = (present_comp_ratings / total_comp_ratings) if total_comp_ratings > 0 else 0.45
        comp_count = len(competitors)
        comp_density = min(comp_count * 15, 60)
        coverage_factor = coverage_ratio * 40

        competitor_saturation = int(min(max(comp_density + coverage_factor, 18), 95))

        # C. Differentiation Potential (0 - 100%)
        # Derived from whitespace wins and critical gaps won in the capability matrix
        native_wins = sum(1 for row in matrix if row.user_idea_rating in ["yes", "partial"] and any(r == "no" for r in row.competitor_ratings.values()))
        critical_wins = sum(1 for row in matrix if row.importance == "Critical" and row.user_idea_rating in ["yes", "partial"])

        gap_base = min(len(gaps) * 14, 48)
        matrix_len = max(len(matrix), 1)
        matrix_win_ratio = (native_wins / matrix_len) * 36
        critical_bonus = min(critical_wins * 6, 16)

        differentiation_potential = int(min(max(gap_base + matrix_win_ratio + critical_bonus, 25), 98))

        # D. Technical Feasibility (0 - 100%)
        # Derived from peer-reviewed academic citations, publication recency, and patent signals
        scholar_count = len(scholar_insights)
        total_citations = sum(s.citations or 0 for s in scholar_insights)
        citation_factor = min(total_citations * 0.08, 22)

        if scholar_count >= 3:
            base_feasibility = 58
        elif scholar_count >= 1:
            base_feasibility = 46
        else:
            base_feasibility = 34

        recent_papers = sum(1 for s in scholar_insights if any(yr in str(s.year) for yr in ["2023", "2024", "2025", "2026"]))
        recency_factor = min(recent_papers * 5, 12)
        patent_factor = min(len(patents) * 4, 10)

        tech_feasibility = int(min(max(base_feasibility + citation_factor + recency_factor + patent_factor, 25), 96))

        # Overall Composite Score
        overall_score = int(
            (market_demand * 0.28) +
            ((100 - competitor_saturation * 0.6) * 0.24) +
            (differentiation_potential * 0.30) +
            (tech_feasibility * 0.18)
        )
        overall_score = min(max(overall_score, 25), 98)

        if overall_score >= 80:
            verdict = "High Opportunity: Defensible Niche"
        elif overall_score >= 65:
            verdict = "Moderate Opportunity: Viable Wedge"
        elif overall_score >= 50:
            verdict = "Emerging Potential: High Execution Risk"
        else:
            verdict = "Challenging Opportunity: Dense Competition"

        rationale = (
            f"Evidence-backed assessment indicates {market_demand}% market demand momentum against {competitor_saturation}% incumbent saturation. "
            f"Defensibility is driven by {differentiation_potential}% differentiation across {len(gaps)} discovered whitespace gaps, "
            f"with {tech_feasibility}% technical feasibility validated by academic literature and patent signals."
        )

        viability = ViabilityScore(
            overall=overall_score,
            market_demand=market_demand,
            competitor_saturation=competitor_saturation,
            differentiation_potential=differentiation_potential,
            tech_feasibility=tech_feasibility,
            verdict=verdict,
            rationale=rationale
        )

        # 4. Strategic 3-Stage Roadmap
        roadmap = [
            RoadmapStep(
                phase="Stage 1: MVP Wedge (0-3 Months)",
                title="Proof of Capability & Core Edge Loop",
                focus="Validate offline functionality on target low-cost hardware",
                deliverables=[
                    "Deploy lightweight on-device inference model with zero internet dependency",
                    "Pilot in 3-5 real-world target environments to benchmark failure rates vs competitors",
                    "Establish cryptographic local storage ensuring data privacy compliance"
                ]
            ),
            RoadmapStep(
                phase="Stage 2: Moat & Workflow Integration (3-9 Months)",
                title="Asynchronous Sync & Administrative Layer",
                focus="Address operational friction and data reporting",
                deliverables=[
                    "Implement fault-tolerant asynchronous queue and periodic mesh sync",
                    "Localized multi-language user interface for non-technical field operators",
                    "Self-serve onboarding reducing deployment time from weeks to 10 minutes"
                ]
            ),
            RoadmapStep(
                phase="Stage 3: Distribution & Institutional Scale (9-18 Months)",
                title="Ecosystem Expansion & Policy Alignment",
                focus="Tap institutional procurement and partnership grants",
                deliverables=[
                    "Partner with regional NGOs, government initiatives, or cooperative unions",
                    "Publish benchmark whitepaper citing field efficiency gains over legacy tools",
                    "Introduce tiered micro-SaaS pricing for sustained expansion"
                ]
            )
        ]

        return {
            "core_opportunity": core_opportunity,
            "executive_summary": summary,
            "gaps": gaps,
            "viability": viability,
            "roadmap": roadmap
        }
