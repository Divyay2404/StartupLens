import re
from typing import List
from app.models.schemas import ResearchPlan, TargetQuery

class QueryPlanner:
    """
    Transforms natural language startup ideas into multi-engine research queries
    for SerpApi (Google Search, News, Scholar, Trends, Patents).
    """

    @staticmethod
    def plan(idea: str, target_region: str = "Global", include_patents: bool = True) -> ResearchPlan:
        clean_idea = idea.strip()
        
        # Extract keywords and domain cues
        words = [w for w in re.findall(r'\b[a-zA-Z0-9_-]+\b', clean_idea.lower()) if len(w) > 2]
        
        # Stop words removal for query construction
        stop_words = {
            "the", "and", "for", "with", "that", "this", "from", "into", "our", "your",
            "system", "tool", "platform", "app", "application", "based", "using", "like", "build"
        }
        key_terms = [w for w in words if w not in stop_words][:6]
        primary_concept = " ".join(key_terms[:3]) if key_terms else clean_idea
        domain = "General Technology"
        target_users = "End-users and organizations"

        # Heuristic domain classification
        lower = clean_idea.lower()
        if any(k in lower for k in ["school", "student", "teacher", "attendance", "education", "classroom"]):
            domain = "EdTech & Computer Vision"
            target_users = "Schools, educators, and rural institutions"
        elif any(k in lower for k in ["soil", "farmer", "crop", "agriculture", "harvest", "field"]):
            domain = "AgriTech & Remote Sensing"
            target_users = "Smallholder farmers, agronomists, and cooperatives"
        elif any(k in lower for k in ["health", "clinic", "patient", "doctor", "triage", "medical"]):
            domain = "HealthTech & Clinical AI"
            target_users = "Clinics, patients, and healthcare workers"
        elif any(k in lower for k in ["food", "restaurant", "bakery", "waste", "surplus", "grocery"]):
            domain = "FoodTech & Supply Chain"
            target_users = "Bakeries, restaurants, and local consumers"
        elif any(k in lower for k in ["legal", "contract", "lawyer", "compliance"]):
            domain = "LegalTech"
            target_users = "Law firms, SMBs, and legal ops"
        elif any(k in lower for k in ["carbon", "energy", "solar", "climate", "emission"]):
            domain = "ClimateTech"
            target_users = "Enterprises, energy operators, and ESG teams"

        queries: List[TargetQuery] = []

        # 1. Google Search: Competitors and products
        queries.append(TargetQuery(
            engine="google",
            query=f"{primary_concept} software competitors alternatives",
            purpose="Identify top commercial competitors, startups, and product offerings"
        ))
        queries.append(TargetQuery(
            engine="google",
            query=f"{clean_idea} solutions pricing features",
            purpose="Analyze pricing models and existing market feature sets"
        ))
        queries.append(TargetQuery(
            engine="google",
            query=f"best tools for {primary_concept}",
            purpose="Discover market incumbents and popular software tools"
        ))

        # 2. Google News: Recent developments, launches, pain points
        queries.append(TargetQuery(
            engine="google_news",
            query=f"{primary_concept} market launches innovation",
            purpose="Track recent venture investments, launches, and market developments"
        ))
        queries.append(TargetQuery(
            engine="google_news",
            query=f"{primary_concept} challenges problems regulation",
            purpose="Uncover emerging pain points, public friction, and regulatory shifts"
        ))

        # 3. Google Scholar: Academic research and state of the art
        queries.append(TargetQuery(
            engine="google_scholar",
            query=f"{primary_concept} algorithms edge lightweight models",
            purpose="Explore state-of-the-art research papers, datasets, and feasibility"
        ))
        queries.append(TargetQuery(
            engine="google_scholar",
            query=f"{primary_concept} framework low resource deployment",
            purpose="Examine academic findings on constraints, latency, and accuracy"
        ))

        # 4. Google Trends: Market interest signals
        trends_term = " ".join(key_terms[:2]) if len(key_terms) >= 2 else primary_concept
        queries.append(TargetQuery(
            engine="google_trends",
            query=trends_term,
            purpose="Gauge search demand velocity, seasonality, and related breakout topics"
        ))

        # 5. Google Patents: IP landscape and prior art
        if include_patents:
            queries.append(TargetQuery(
                engine="google_patents",
                query=f"system and method for {primary_concept}",
                purpose="Evaluate technical patent landscape and proprietary claims"
            ))

        return ResearchPlan(
            summary=f"Automated multi-engine research plan targeting {domain}. Dispatches 5 engines via SerpApi to triangulate existing competitors, academic foundations, news sentiment, and search demand.",
            core_domain=domain,
            target_users=target_users,
            queries=queries
        )
