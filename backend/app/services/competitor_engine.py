from typing import List, Dict, Any
from urllib.parse import urlparse
from app.models.schemas import CompetitorItem, MatrixFeatureRow, SearchEvidenceItem

class CompetitorEngine:
    """
    Extracts competitors, profiles capabilities, and builds the Killer Feature:
    Opportunity Gap Feature Comparison Matrix (Competitors vs User Idea).
    """

    @staticmethod
    def extract_competitors_and_matrix(
        idea: str,
        evidence_items: List[SearchEvidenceItem],
        domain: str
    ) -> Dict[str, Any]:
        idea_lower = idea.lower()
        competitors: List[CompetitorItem] = []
        
        # 1. Extract competitors from Search Evidence
        product_items = [item for item in evidence_items if item.engine == "google"]
        
        for item in product_items[:4]:
            parsed = urlparse(item.link)
            domain_name = parsed.netloc.replace("www.", "")
            name = item.title.split("-")[0].split("|")[0].split(":")[0].strip()
            if not name or len(name) < 3:
                name = domain_name.capitalize() if domain_name else "Competitor Solution"
            
            # Avoid duplicate competitor names
            if any(c.name.lower() == name.lower() for c in competitors):
                continue

            # Infer competitor characteristics from snippets
            snippet_lower = item.snippet.lower()
            strengths = []
            weaknesses = []
            
            if any(k in snippet_lower for k in ["cloud", "enterprise", "managed", "corporate", "portal"]):
                strengths.append("Established enterprise infrastructure and brand visibility")
                weaknesses.append("Heavy reliance on continuous internet connectivity")
            else:
                strengths.append("Specialized feature workflow")
                weaknesses.append("High implementation friction")

            if any(k in snippet_lower for k in ["$", "pricing", "license", "expensive", "cost"]):
                weaknesses.append("Expensive pricing tier inaccessible to budget-sensitive users")
            else:
                weaknesses.append("Limited transparency around deployment costs")

            if any(k in snippet_lower for k in ["hardware", "camera", "terminal", "device"]):
                strengths.append("Dedicated proprietary hardware ecosystem")
                weaknesses.append("High capital expenditure and maintenance requirements")

            competitors.append(CompetitorItem(
                name=name,
                url=item.link,
                summary=item.snippet[:160] + "..." if len(item.snippet) > 160 else item.snippet,
                target_audience="Enterprise and urban tier-1 organizations",
                pricing_model="Enterprise SaaS / Proprietary hardware licenses",
                strengths=strengths or ["Market incumbent", "Feature-dense"],
                weaknesses=weaknesses or ["Not optimized for low-connectivity environments", "High onboarding barrier"]
            ))

        # Guarantee at least 3 competitors for robust matrix comparison
        if len(competitors) < 3:
            CompetitorEngine._pad_default_competitors(competitors, idea_lower)

        # 2. Extract domain-specific feature dimensions for the Matrix
        matrix_rows = CompetitorEngine._build_feature_matrix(idea_lower, competitors)

        return {
            "competitors": competitors,
            "matrix": matrix_rows
        }

    @staticmethod
    def _pad_default_competitors(competitors: List[CompetitorItem], idea_lower: str):
        if "attendance" in idea_lower or "school" in idea_lower:
            defaults = [
                CompetitorItem(
                    name="Verkada Cloud Face Terminal",
                    url="https://www.verkada.com",
                    summary="Enterprise cloud-connected facial recognition cameras for schools. Requires 1Gbps bandwidth and $1,500/year license.",
                    target_audience="High-budget urban school districts",
                    pricing_model="$1,500/yr per camera",
                    strengths=["Centralized administration", "Polished security dashboard"],
                    weaknesses=["Completely inoperable offline", "Prohibitive costs for rural schools", "Cloud privacy concerns"]
                ),
                CompetitorItem(
                    name="SmartSchool Portal App",
                    url="https://example.com/smart-school",
                    summary="Cloud mobile attendance check-in application requiring smartphones for all students.",
                    target_audience="Private colleges and universities",
                    pricing_model="$8/student/month",
                    strengths=["Mobile app UX", "Parent notification SMS"],
                    weaknesses=["Requires individual 4G smartphones", "Fails in zero-connectivity zones"]
                ),
                CompetitorItem(
                    name="Hikvision DS Biometric Terminal",
                    url="https://www.hikvision.com",
                    summary="Standalone biometric and facial terminal for office and campus entry gates.",
                    target_audience="Large physical campuses",
                    pricing_model="$650 one-off hardware",
                    strengths=["Fast indoor recognition", "Durable casing"],
                    weaknesses=["Requires fixed electrical wiring", "Complex technician setup", "No edge analytics"]
                )
            ]
        else:
            defaults = [
                CompetitorItem(
                    name="Incumbent Enterprise Suite",
                    url="https://example.com/enterprise-incumbent",
                    summary="Legacy corporate software covering standard workflows with heavy setup requirements.",
                    target_audience="Global enterprise accounts",
                    pricing_model="Annual contract with seat licenses",
                    strengths=["Brand trust", "Compliance certifications"],
                    weaknesses=["Slow, bloated user experience", "Lack of offline or edge support", "Expensive"]
                ),
                CompetitorItem(
                    name="Generic Cloud SaaS",
                    url="https://example.com/cloud-saas",
                    summary="Web-only platform providing standard cloud automation without specialized vertical features.",
                    target_audience="Mid-market teams",
                    pricing_model="Monthly subscription",
                    strengths=["Quick self-service signup", "Standard integrations"],
                    weaknesses=["Requires constant internet", "Generic features, ignores niche constraints"]
                ),
                CompetitorItem(
                    name="Open Source DIY Framework",
                    url="https://github.com",
                    summary="Code repositories and libraries requiring custom engineering and self-hosting.",
                    target_audience="Software developers",
                    pricing_model="Free (High engineering overhead)",
                    strengths=["Full code control", "No subscription"],
                    weaknesses=["High technical skill barrier", "No turnkey reliability or customer support"]
                )
            ]

        for d in defaults:
            if not any(c.name.lower() == d.name.lower() for c in competitors):
                competitors.append(d)
            if len(competitors) >= 3:
                break

    @staticmethod
    def _evaluate_user_capability(feature_name: str, idea_lower: str, category: str = "") -> str:
        """
        Evaluates whether the user's startup idea genuinely supports a capability.
        Returns:
            - 'yes' (Native): Explicit evidence or claims in the idea description.
            - 'partial' (Partial): Partial context, related domain, or indirect support.
            - 'unverified': Insufficient evidence or unstated capability (safe fallback).
        """
        f_lower = feature_name.lower()

        # 1. Offline & Edge capabilities
        if any(k in f_lower for k in ["offline", "edge"]):
            if any(k in idea_lower for k in ["offline", "low-connectivity", "no internet", "no-connectivity", "off-grid", "mesh sync", "mesh"]):
                return "yes"
            if any(k in idea_lower for k in ["edge", "on-device", "local queue", "rural", "remote"]):
                return "partial"
            return "unverified"

        # 2. Biometric & Data Privacy capabilities
        if any(k in f_lower for k in ["privacy", "sovereignty", "local data"]):
            if any(k in idea_lower for k in ["privacy", "on-device", "local storage", "sovereignty", "encrypted", "no cloud"]):
                return "yes"
            if any(k in idea_lower for k in ["facial", "biometric", "attendance", "sensitive"]):
                return "partial"
            return "unverified"

        # 3. Hardware Cost & Affordability capabilities
        if any(k in f_lower for k in ["hardware", "pricing", "cost", "affordable", "tier"]):
            if any(k in idea_lower for k in ["affordable", "low cost", "low-cost", "budget", "sub-$", "inexpensive", "free", "$50", "$1", "cheap"]):
                return "yes"
            if any(k in idea_lower for k in ["rural", "smallholder", "micro", "underserved", "schools"]):
                return "partial"
            return "unverified"

        # 4. Rural, Smallholder & Vertical Niche Focus
        if any(k in f_lower for k in ["rural", "low-connectivity focus", "niche", "customization"]):
            if any(k in idea_lower for k in ["rural", "remote", "village", "smallholder", "niche", "customized", "vertical", "surplus"]):
                return "yes"
            return "unverified"

        # 5. Multilingual & Local Dialect UI
        if any(k in f_lower for k in ["dialect", "multilingual", "language"]):
            if any(k in idea_lower for k in ["dialect", "vernacular", "multilingual", "local language", "translation", "voice"]):
                return "yes"
            return "unverified"

        # 6. Power Tolerance & Resilience
        if any(k in f_lower for k in ["solar", "power", "electricity"]):
            if any(k in idea_lower for k in ["solar", "intermittent power", "power cut", "battery", "low power", "electricity", "resilient"]):
                return "yes"
            return "unverified"

        # 7. Optical / Camera Diagnostic
        if any(k in f_lower for k in ["camera", "diagnostic", "optical", "smartphone"]):
            if any(k in idea_lower for k in ["camera", "smartphone", "phone", "optical", "scanner", "scan"]):
                return "yes"
            if any(k in idea_lower for k in ["mobile", "app", "instant"]):
                return "partial"
            return "unverified"

        # 8. Organic / Local Fertilizer Advice
        if any(k in f_lower for k in ["fertilizer", "soil", "nutrient"]):
            if any(k in idea_lower for k in ["fertilizer", "nutrient", "npk", "soil health", "soil"]):
                return "yes"
            return "unverified"

        # 9. Lightweight / Frictionless Setup
        if any(k in f_lower for k in ["friction", "setup", "lightweight"]):
            if any(k in idea_lower for k in ["friction", "turnkey", "lightweight", "instant setup", "no install", "plug and play"]):
                return "yes"
            return "unverified"

        # Generic heuristic fallback based on token overlap
        tokens = [t for t in f_lower.replace("/", " ").replace("-", " ").split() if len(t) > 3 and t not in ["operation", "mode", "setup", "core", "focus"]]
        matched_tokens = sum(1 for t in tokens if t in idea_lower)
        if matched_tokens >= 2:
            return "yes"
        elif matched_tokens == 1:
            return "partial"

        return "unverified"

    @staticmethod
    def _build_feature_matrix(idea_lower: str, competitors: List[CompetitorItem]) -> List[MatrixFeatureRow]:
        """
        Creates the Killer Feature Matrix: Feature vs Competitors vs User Idea
        Values: 'yes' (✓), 'no' (✗), 'partial' (■), 'unverified' (?)
        """
        comp_names = [c.name for c in competitors[:3]]
        
        if "attendance" in idea_lower or "school" in idea_lower or "rural" in idea_lower:
            features_def = [
                {
                    "name": "Offline-First Operation",
                    "category": "Core Architecture",
                    "importance": "Critical",
                    "ratings": {comp_names[0]: "no", comp_names[1]: "no", comp_names[2]: "partial"} if len(comp_names) >= 3 else {},
                    "reason": "Existing systems break entirely when internet drops. An offline-first local queue enables seamless morning roll calls in remote areas."
                },
                {
                    "name": "On-Device Biometric Privacy",
                    "category": "Data Sovereignty",
                    "importance": "Critical",
                    "ratings": {comp_names[0]: "partial", comp_names[1]: "no", comp_names[2]: "partial"} if len(comp_names) >= 3 else {},
                    "reason": "Centralized student photos risk regulatory backlash. Local vector embeddings eliminate cloud image storage vulnerabilities."
                },
                {
                    "name": "Sub-$50 Hardware Barrier",
                    "category": "Affordability",
                    "importance": "High",
                    "ratings": {comp_names[0]: "no", comp_names[1]: "partial", comp_names[2]: "no"} if len(comp_names) >= 3 else {},
                    "reason": "Incumbent biometric systems cost $600-$1,500+. Running on budget Android tablets or Raspberry Pis democratizes adoption."
                },
                {
                    "name": "Rural & Low-Connectivity Focus",
                    "category": "Market Positioning",
                    "importance": "High",
                    "ratings": {comp_names[0]: "no", comp_names[1]: "no", comp_names[2]: "no"} if len(comp_names) >= 3 else {},
                    "reason": "Zero major competitors design specifically for rural infrastructure constraints; all focus on metropolitan corporate/school buyers."
                },
                {
                    "name": "Local Dialect & Multilingual UI",
                    "category": "Usability",
                    "importance": "Medium",
                    "ratings": {comp_names[0]: "partial", comp_names[1]: "no", comp_names[2]: "no"} if len(comp_names) >= 3 else {},
                    "reason": "Non-English local school staff struggle with complex English-only dashboards."
                },
                {
                    "name": "Solar / Intermittent Power Tolerant",
                    "category": "Resilience",
                    "importance": "High",
                    "ratings": {comp_names[0]: "no", comp_names[1]: "no", comp_names[2]: "partial"} if len(comp_names) >= 3 else {},
                    "reason": "Operates with ultra-low power consumption and automatic resume on power fluctuations."
                }
            ]
        elif "soil" in idea_lower or "farm" in idea_lower or "agri" in idea_lower:
            features_def = [
                {
                    "name": "Instant Smartphone Camera Diagnostic",
                    "category": "Accessibility",
                    "importance": "Critical",
                    "ratings": {comp_names[0]: "no", comp_names[1]: "partial", comp_names[2]: "no"} if len(comp_names) >= 3 else {},
                    "reason": "Competitors require $3,000 spectrometer hardware or laboratory mail-in testing taking weeks."
                },
                {
                    "name": "Affordable Per-Test Cost (<$1)",
                    "category": "Economics",
                    "importance": "Critical",
                    "ratings": {comp_names[0]: "no", comp_names[1]: "partial", comp_names[2]: "no"} if len(comp_names) >= 3 else {},
                    "reason": "Smallholder farmers cannot afford expensive recurring lab fees."
                },
                {
                    "name": "Offline Field Inference",
                    "category": "Core Architecture",
                    "importance": "High",
                    "ratings": {comp_names[0]: "no", comp_names[1]: "no", comp_names[2]: "partial"} if len(comp_names) >= 3 else {},
                    "reason": "Farmland has poor cellular reception; on-device neural nets run anywhere."
                },
                {
                    "name": "Actionable Organic & Local Fertilizer Advice",
                    "category": "Output Relevance",
                    "importance": "High",
                    "ratings": {comp_names[0]: "partial", comp_names[1]: "partial", comp_names[2]: "no"} if len(comp_names) >= 3 else {},
                    "reason": "Translates chemical metrics into exact indigenous soil amendments farmers can actually buy."
                }
            ]
        else:
            features_def = [
                {
                    "name": "Offline-First / Edge Autonomous Mode",
                    "category": "Core Architecture",
                    "importance": "Critical",
                    "ratings": {comp_names[0]: "no", comp_names[1]: "no", comp_names[2]: "partial"} if len(comp_names) >= 3 else {},
                    "reason": "Competitors are heavily cloud-dependent; edge capability enables uninterrupted workflows."
                },
                {
                    "name": "Hyper-Affordable Pricing for Underserved Segments",
                    "category": "Distribution",
                    "importance": "High",
                    "ratings": {comp_names[0]: "no", comp_names[1]: "partial", comp_names[2]: "no"} if len(comp_names) >= 3 else {},
                    "reason": "Incumbents target well-funded corporate budgets, ignoring price-sensitive small operators."
                },
                {
                    "name": "Lightweight Zero-Friction Setup",
                    "category": "User Experience",
                    "importance": "High",
                    "ratings": {comp_names[0]: "partial", comp_names[1]: "no", comp_names[2]: "partial"} if len(comp_names) >= 3 else {},
                    "reason": "Eliminates months-long IT onboarding with self-contained, turnkey design."
                },
                {
                    "name": "Tailored Vertical Niche Customization",
                    "category": "Product Strategy",
                    "importance": "Critical",
                    "ratings": {comp_names[0]: "no", comp_names[1]: "no", comp_names[2]: "no"} if len(comp_names) >= 3 else {},
                    "reason": "Horizontal competitors provide broad generic software that fails to solve specific edge cases."
                },
                {
                    "name": "Privacy-Preserving Local Data Storage",
                    "category": "Security & Trust",
                    "importance": "High",
                    "ratings": {comp_names[0]: "partial", comp_names[1]: "no", comp_names[2]: "partial"} if len(comp_names) >= 3 else {},
                    "reason": "Sensitive user data stays on device rather than being aggregated in third-party cloud data centers."
                }
            ]

        rows = []
        for f in features_def:
            ratings = {}
            for idx, c in enumerate(competitors[:3]):
                c_rating = f["ratings"].get(c.name)
                if not c_rating:
                    # Deterministic default assignment
                    c_rating = "no" if idx == 0 else ("partial" if idx == 1 else "no")
                ratings[c.name] = c_rating

            user_rating = CompetitorEngine._evaluate_user_capability(
                feature_name=f["name"],
                idea_lower=idea_lower,
                category=f.get("category", "")
            )

            rows.append(MatrixFeatureRow(
                feature_name=f["name"],
                category=f["category"],
                importance=f["importance"],
                competitor_ratings=ratings,
                user_idea_rating=user_rating,
                opportunity_reason=f["reason"]
            ))

        return rows