import re
from typing import List, Dict, Any, Optional, Set
from urllib.parse import urlparse
from app.models.schemas import CompetitorItem, MatrixFeatureRow, SearchEvidenceItem

NON_PRODUCT_DOMAINS: Set[str] = {
    "wikipedia.org", "wikimedia.org", "youtube.com", "youtu.be", "medium.com",
    "reddit.com", "quora.com", "github.com", "gist.github.com", "gitlab.com",
    "forbes.com", "techcrunch.com", "bloomberg.com", "nytimes.com", "wsj.com",
    "businessinsider.com", "cnbc.com", "theverge.com", "wired.com", "venturebeat.com",
    "linkedin.com", "twitter.com", "x.com", "facebook.com", "instagram.com",
    "pinterest.com", "tiktok.com", "amazon.com", "ebay.com", "walmart.com",
    "play.google.com", "apps.apple.com", "arxiv.org", "sciencedirect.com",
    "researchgate.net", "semanticscholar.org", "springer.com", "nature.com",
    "google.com", "bing.com", "yahoo.com", "duckduckgo.com", "producthunt.com",
    "capterra.com", "g2.com", "trustradius.com", "softwareadvice.com",
    "investopedia.com", "statista.com", "coursera.org", "udemy.com"
}

INFORMATIONAL_PREFIXES = (
    "top ", "10 best", "5 best", "best ", "how to", "what is", "why you",
    "guide to", "an overview", "a review", "review:", "vs ", "versus ",
    "definition", "introduction to", "tutorial", "the future of", "trends in"
)


class CompetitorEngine:
    """
    Extracts competitors, profiles capabilities, and builds the Killer Feature:
    Opportunity Gap Feature Comparison Matrix (Competitors vs User Idea).
    Ensures competitors strictly reflect the startup's industry, functionality, and target audience.
    """

    @staticmethod
    def _is_valid_competitor_domain(link: str) -> bool:
        if not link:
            return False
        parsed = urlparse(link)
        domain = parsed.netloc.lower().replace("www.", "")
        if any(npd in domain for npd in NON_PRODUCT_DOMAINS):
            return False
        return True

    @staticmethod
    def _is_informational_title(title: str) -> bool:
        lower = title.lower().strip()
        if any(lower.startswith(prefix) for prefix in INFORMATIONAL_PREFIXES):
            return True
        if any(phrase in lower for phrase in ["top 10", "10 best", "best tools for", "how to choose", "free download", "beginners guide"]):
            return True
        return False

    @staticmethod
    def _clean_competitor_name(title: str, domain_name: str) -> str:
        cleaned = title.strip()
        for separator in [" - ", " | ", " : ", " — ", " – "]:
            if separator in cleaned:
                parts = [p.strip() for p in cleaned.split(separator) if p.strip()]
                clean_dom = domain_name.split(".")[0].lower()
                matching_part = next((p for p in parts if clean_dom in p.lower() and 3 <= len(p) <= 30), None)
                if matching_part:
                    cleaned = matching_part
                    break
                else:
                    valid_parts = [p for p in parts if len(p) >= 3 and not CompetitorEngine._is_informational_title(p)]
                    cleaned = valid_parts[0] if valid_parts else parts[0]
                break

        words = cleaned.split()
        if len(words) > 5 or len(cleaned) > 35 or len(cleaned) < 3 or CompetitorEngine._is_informational_title(cleaned):
            base = domain_name.split(".")[0]
            cleaned = base.replace("-", " ").title()

        return cleaned

    @staticmethod
    def _calculate_relevance(item: SearchEvidenceItem, idea: str, domain: str, target_users: str) -> float:
        score = 0.0
        text = f"{item.title} {item.snippet}".lower()
        parsed = urlparse(item.link)
        domain_name = parsed.netloc.lower().replace("www.", "")

        stop_words = {"the", "and", "for", "with", "that", "this", "from", "into", "our", "your", "system", "tool", "platform", "app"}
        idea_words = [w for w in re.findall(r'\b[a-zA-Z0-9_-]+\b', idea.lower()) if len(w) > 2 and w not in stop_words]
        domain_words = [w for w in re.findall(r'\b[a-zA-Z0-9_-]+\b', domain.lower()) if len(w) > 2 and w not in stop_words]
        user_words = [w for w in re.findall(r'\b[a-zA-Z0-9_-]+\b', (target_users or "").lower()) if len(w) > 2 and w not in stop_words]

        # 1. Match core idea keywords
        idea_matches = sum(1 for w in idea_words if w in text)
        score += idea_matches * 2.5

        # 2. Match industry / domain keywords
        domain_matches = sum(1 for w in domain_words if w in text)
        score += domain_matches * 1.8

        # 3. Match target user context
        user_matches = sum(1 for w in user_words if w in text)
        score += user_matches * 1.2

        # 4. Commercial product signal bonus
        product_signals = ["software", "platform", "solution", "app", "tool", "pricing", "features", "devices", "hardware", "terminal", "portal", "cloud", "saas", "scanner", "dashboard"]
        if any(sig in text for sig in product_signals):
            score += 2.0

        # 5. Informational content penalty
        if CompetitorEngine._is_informational_title(item.title):
            score -= 4.0
        if any(info in text for info in ["published", "read article", "blog post", "whitepaper", "research paper", "forum", "news update"]):
            score -= 2.0

        # 6. Domain name relevance
        if any(w in domain_name for w in idea_words[:3]):
            score += 2.0

        return score

    @staticmethod
    def _infer_target_audience(domain: str, target_users: Optional[str], snippet: str) -> str:
        s_lower = snippet.lower()
        if "enterprise" in s_lower or "corporate" in s_lower or "fortune" in s_lower:
            return "Large corporate accounts and tier-1 institutions"
        if "smb" in s_lower or "small business" in s_lower:
            return "Commercial small and medium-sized businesses"

        if target_users and len(target_users) > 5:
            return f"Established mainstream {target_users.lower()}"

        d_lower = (domain or "").lower()
        if "edtech" in d_lower or "education" in d_lower:
            return "Urban school districts and higher education campuses"
        if "agritech" in d_lower or "agri" in d_lower:
            return "Commercial agribusinesses, cooperatives, and agronomy labs"
        if "food" in d_lower:
            return "Commercial restaurant chains, wholesale bakeries, and grocery retailers"
        if "health" in d_lower:
            return "Metropolitan hospital networks and centralized health systems"
        if "legal" in d_lower:
            return "Corporate legal operations and large law firms"
        if "climate" in d_lower:
            return "Utility operators and enterprise ESG compliance teams"

        return "Enterprise and mainstream market organizations"

    @staticmethod
    def _infer_strengths_weaknesses(snippet: str, domain: str) -> tuple[List[str], List[str]]:
        s_lower = snippet.lower()
        strengths = []
        weaknesses = []

        if any(k in s_lower for k in ["cloud", "portal", "dashboard", "centralized"]):
            strengths.append("Established centralized cloud management and polished web dashboards")
            weaknesses.append("High dependence on persistent high-speed internet connectivity")
        elif any(k in s_lower for k in ["hardware", "camera", "terminal", "device", "scanner"]):
            strengths.append("Proprietary hardware integration and dedicated physical sensors")
            weaknesses.append("High upfront capital cost and complex technician installation")
        elif any(k in s_lower for k in ["mobile", "app", "ios", "android"]):
            strengths.append("Broad mobile application distribution and smartphone accessibility")
            weaknesses.append("Requires expensive personal smartphones; lacks on-device offline inference")
        else:
            strengths.append("Established brand visibility and comprehensive general feature set")
            weaknesses.append("Rigid horizontal workflows; lacks optimization for localized edge constraints")

        if any(k in s_lower for k in ["$", "pricing", "license", "expensive", "contract", "enterprise"]):
            weaknesses.append("Expensive recurring licensing overhead prohibitive to budget-conscious users")
        else:
            weaknesses.append("Lack of transparent self-serve pricing; requires lengthy procurement")

        return strengths, weaknesses

    @staticmethod
    def extract_competitors_and_matrix(
        idea: str,
        evidence_items: List[SearchEvidenceItem],
        domain: str,
        target_users: Optional[str] = None
    ) -> Dict[str, Any]:
        idea_lower = idea.lower()
        competitors: List[CompetitorItem] = []

        # 1. Filter, score, and rank search evidence items
        google_items = [
            item for item in evidence_items
            if item.engine == "google" and CompetitorEngine._is_valid_competitor_domain(item.link)
        ]

        scored_items = []
        for item in google_items:
            score = CompetitorEngine._calculate_relevance(item, idea, domain, target_users or "")
            if score >= 2.0:
                scored_items.append((score, item))

        # Sort by relevance descending
        scored_items.sort(key=lambda x: x[0], reverse=True)

        for _, item in scored_items:
            parsed = urlparse(item.link)
            domain_name = parsed.netloc.replace("www.", "")
            name = CompetitorEngine._clean_competitor_name(item.title, domain_name)

            if not name or len(name) < 3:
                name = domain_name.capitalize() if domain_name else "Competitor Solution"

            # Avoid duplicates
            if any(c.name.lower() == name.lower() or (c.url and urlparse(c.url).netloc == urlparse(item.link).netloc) for c in competitors):
                continue

            target_audience = CompetitorEngine._infer_target_audience(domain, target_users, item.snippet)
            strengths, weaknesses = CompetitorEngine._infer_strengths_weaknesses(item.snippet, domain)

            pricing_model = "Enterprise SaaS / Subscription"
            if any(k in item.snippet.lower() for k in ["hardware", "terminal", "device"]):
                pricing_model = "Proprietary hardware + maintenance fee"
            elif any(k in item.snippet.lower() for k in ["free", "freemium", "open source"]):
                pricing_model = "Freemium / Open Core"

            competitors.append(CompetitorItem(
                name=name,
                url=item.link,
                summary=item.snippet[:160] + "..." if len(item.snippet) > 160 else item.snippet,
                target_audience=target_audience,
                pricing_model=pricing_model,
                strengths=strengths,
                weaknesses=weaknesses
            ))

            if len(competitors) >= 3:
                break

        # Guarantee at least 3 relevant competitors using domain-aware fallback if search evidence is sparse
        if len(competitors) < 3:
            CompetitorEngine._pad_default_competitors(competitors, idea_lower, domain, target_users)

        # 2. Extract domain-specific feature dimensions for the Matrix
        matrix_rows = CompetitorEngine._build_feature_matrix(idea_lower, competitors)

        return {
            "competitors": competitors,
            "matrix": matrix_rows
        }

    @staticmethod
    def _pad_default_competitors(
        competitors: List[CompetitorItem],
        idea_lower: str,
        domain: str = "",
        target_users: Optional[str] = None
    ):
        defaults: List[CompetitorItem] = []

        # 1. EdTech / Attendance / Biometrics
        if ("attendance" in idea_lower or "roll call" in idea_lower) or ("school" in idea_lower and any(k in idea_lower for k in ["biometric", "facial", "card", "entry"])):
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

        # 2. AgriTech / Soil / Farming
        elif any(k in idea_lower for k in ["soil", "farm", "agri", "crop", "fertilizer"]):
            defaults = [
                CompetitorItem(
                    name="AgroCares Handheld Scanner",
                    url="https://www.agrocares.com",
                    summary="Near-infrared handheld spectrometer testing NPK and soil pH with proprietary laboratory calibration.",
                    target_audience="Commercial agribusinesses and agricultural research institutes",
                    pricing_model="$3,500 hardware + $150/mo subscription",
                    strengths=["Laboratory-grade spectroscopic accuracy", "Extensive chemical database"],
                    weaknesses=["Prohibitive cost for smallholders", "Requires specialized sensor maintenance"]
                ),
                CompetitorItem(
                    name="CropIn SmartFarm AI",
                    url="https://www.cropin.com",
                    summary="Enterprise satellite imagery and agronomy platform monitoring macro crop health and yield prediction.",
                    target_audience="Corporate farms and multinational food suppliers",
                    pricing_model="Annual enterprise license",
                    strengths=["Macro satellite monitoring", "Comprehensive ESG reporting"],
                    weaknesses=["Cannot analyze subsurface micro-nutrients", "Geared for industrial operations"]
                ),
                CompetitorItem(
                    name="Plantix Mobile Crop Doctor",
                    url="https://plantix.net",
                    summary="Smartphone camera app detecting visible plant foliar diseases and pest damage.",
                    target_audience="Individual farmers and extension workers",
                    pricing_model="Freemium ad-supported",
                    strengths=["Smartphone camera accessibility", "Visual pest diagnostics"],
                    weaknesses=["Lacks chemical soil nutrient testing", "Does not diagnose soil NPK deficiencies"]
                )
            ]

        # 3. FoodTech / Bakery / Surplus / Food Waste
        elif any(k in idea_lower for k in ["bakery", "surplus", "food waste", "restaurant", "grocery"]):
            defaults = [
                CompetitorItem(
                    name="Too Good To Go Surplus App",
                    url="https://toogoodtogo.com",
                    summary="Consumer-facing surprise bag marketplace connecting retail cafes to local consumers for end-of-day surplus.",
                    target_audience="Urban retail bakeries and consumer bargain shoppers",
                    pricing_model="Transaction commission per mystery bag",
                    strengths=["Consumer brand recognition", "Immediate consumer foot traffic"],
                    weaknesses=["Unpredictable mystery-bag model", "Lacks B2B cafe-to-shelter batch clearance logistics"]
                ),
                CompetitorItem(
                    name="Sysco / Commercial Food Distributor",
                    url="https://www.sysco.com",
                    summary="Wholesale inventory supply chain managing scheduled institutional deliveries with bulk returns.",
                    target_audience="Commercial food service chains and hotels",
                    pricing_model="Wholesale volume contracts",
                    strengths=["Massive cold storage logistics", "Established purchasing contracts"],
                    weaknesses=["Slow multi-day delivery turnaround", "Incompatible with perishable 1-hour bakery surplus"]
                ),
                CompetitorItem(
                    name="Manual End-of-Day Markdown System",
                    url="https://example.com/manual-clearing",
                    summary="Traditional ad-hoc shelf markdown stickers and staff discretion discounting 30 minutes before closing.",
                    target_audience="Independent neighborhood bakeries",
                    pricing_model="Zero software fee (Manual labor overhead)",
                    strengths=["No software learning curve", "Immediate cashier execution"],
                    weaknesses=["High unsold dump rates (15-25%)", "Zero demand broadcasting outside the store"]
                )
            ]

        # 4. HealthTech / Telehealth / Voice AI / Senior Triage
        elif any(k in idea_lower for k in ["health", "triage", "senior", "clinic", "telehealth", "patient", "medical"]):
            defaults = [
                CompetitorItem(
                    name="Teladoc Health Virtual Clinic",
                    url="https://www.teladoc.com",
                    summary="Nationwide video telehealth platform connecting insured patients with remote physicians.",
                    target_audience="Corporate health plan members and insured urban patients",
                    pricing_model="Enterprise employer contracts + copays",
                    strengths=["Large certified physician network", "Direct EHR integration"],
                    weaknesses=["Requires high-speed video data and smartphone literacy", "English-centric, inaccessible to rural seniors"]
                ),
                CompetitorItem(
                    name="Epic Systems MyChart Patient Portal",
                    url="https://www.epic.com",
                    summary="Comprehensive hospital portal providing patient chart access, secure messaging, and appointment scheduling.",
                    target_audience="Hospital networks and health system patients",
                    pricing_model="Multi-million dollar hospital licensing",
                    strengths=["Deep clinical record integration", "Comprehensive diagnostic history"],
                    weaknesses=["Complex multi-step web authentication", "Intimidating interface for non-digital seniors"]
                ),
                CompetitorItem(
                    name="Legacy Nurse Triage Phone Hotline",
                    url="https://example.com/nurse-line",
                    summary="Centralized 24/7 call center staffed by registered nurses using standardized triage scripts.",
                    target_audience="Health insurance subscribers",
                    pricing_model="Covered under insurance overhead",
                    strengths=["Accessible over standard telephony", "Empathetic human consultation"],
                    weaknesses=["Long wait and hold times (25+ mins)", "Lacks vernacular dialect recognition; high staffing costs"]
                )
            ]

        # 5. LegalTech / Contracts
        elif any(k in idea_lower for k in ["legal", "contract", "lawyer", "compliance"]):
            defaults = [
                CompetitorItem(
                    name="Ironclad Contract Lifecycle Suite",
                    url="https://ironcladapp.com",
                    summary="Enterprise contract management and workflow platform automating approvals for corporate legal ops.",
                    target_audience="Corporate legal departments and enterprise procurement",
                    pricing_model="Enterprise annual contracts ($20k+/yr)",
                    strengths=["Complex workflow orchestration", "Salesforce and ERP connectors"],
                    weaknesses=["Prohibitive cost for small businesses", "Requires months of administrator configuration"]
                ),
                CompetitorItem(
                    name="LegalZoom Template Directory",
                    url="https://www.legalzoom.com",
                    summary="Self-service legal document library offering standard pre-drafted templates for common agreements.",
                    target_audience="Sole proprietors and micro-businesses",
                    pricing_model="Per-document purchase ($30-$150)",
                    strengths=["Affordable per-document pricing", "Standard legal boilerplate"],
                    weaknesses=["Static templates with zero contextual risk analysis", "No AI redlining or counterparty review"]
                ),
                CompetitorItem(
                    name="Traditional Retainer Law Firm",
                    url="https://example.com/law-firm",
                    summary="Conventional hourly attorney advisory services reviewing bespoke agreements.",
                    target_audience="Mid-market to enterprise companies",
                    pricing_model="Hourly billable rate ($400-$800/hr)",
                    strengths=["Defensible legal liability coverage", "Bespoke nuance interpretation"],
                    weaknesses=["Slow multi-day turnarounds", "Extremely expensive billable hours for routine reviews"]
                )
            ]

        # 6. Dynamic domain-specific synthesis for arbitrary startup ideas
        else:
            words = [w for w in idea_lower.split() if len(w) > 3 and w not in ["with", "that", "this", "from", "into", "your", "system", "tool", "platform"]][:3]
            concept = " ".join(words).title() if words else "Industry"
            industry = domain.split("&")[0].strip() if domain else "Commercial"
            target = target_users or "Enterprise Organizations"

            defaults = [
                CompetitorItem(
                    name=f"Enterprise {concept} Incumbent",
                    url=f"https://example.com/{'-'.join(words)}-enterprise",
                    summary=f"Legacy {industry} software suite providing standard {concept.lower()} workflows with annual enterprise contracts.",
                    target_audience=f"Tier-1 corporate buyers in {target.lower()}",
                    pricing_model="Annual contract with seat licensing",
                    strengths=["Established brand trust", "Broad standard compliance certifications"],
                    weaknesses=["Bloated multi-tab interface", "Slow onboarding cycles", "Lacks tailored edge workflows"]
                ),
                CompetitorItem(
                    name=f"Generic Cloud {concept} SaaS",
                    url=f"https://example.com/{'-'.join(words)}-cloud",
                    summary=f"Horizontal cloud-only automation platform covering general-purpose {concept.lower()} without vertical customization.",
                    target_audience=f"Mainstream mid-market {target.lower()}",
                    pricing_model="Monthly subscription",
                    strengths=["Quick self-service signup", "Standard cloud integrations"],
                    weaknesses=["Requires continuous internet", "Generic feature set ignoring specialized niche constraints"]
                ),
                CompetitorItem(
                    name=f"Manual / Fragmented {concept} Process",
                    url=f"https://example.com/{'-'.join(words)}-manual",
                    summary=f"Traditional manual operations relying on spreadsheets, phone coordination, and physical documentation for {concept.lower()}.",
                    target_audience=f"Traditional operators in {target.lower()}",
                    pricing_model="Zero software cost (High human labor overhead)",
                    strengths=["Zero software learning curve", "Total operational familiarity"],
                    weaknesses=["High error rates and latency", "Zero automated intelligence or real-time synchronization"]
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

        if ("attendance" in idea_lower or "roll call" in idea_lower) or ("school" in idea_lower and any(k in idea_lower for k in ["biometric", "facial", "card", "entry"])):
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
        elif any(k in idea_lower for k in ["soil", "farm", "agri", "crop", "fertilizer"]):
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
        elif any(k in idea_lower for k in ["bakery", "surplus", "food waste", "restaurant", "grocery"]):
            features_def = [
                {
                    "name": "Sub-60 Minute Real-Time Clearing",
                    "category": "Velocity",
                    "importance": "Critical",
                    "ratings": {comp_names[0]: "partial", comp_names[1]: "no", comp_names[2]: "no"} if len(comp_names) >= 3 else {},
                    "reason": "Incumbents require hours of lead time or next-day scheduled pickup, letting fresh evening bakery goods expire."
                },
                {
                    "name": "Hyperlocal Micro-Marketplace Density",
                    "category": "Distribution",
                    "importance": "Critical",
                    "ratings": {comp_names[0]: "partial", comp_names[1]: "no", comp_names[2]: "no"} if len(comp_names) >= 3 else {},
                    "reason": "Wholesale distributors cannot service individual blocks; hyperlocal matching keeps transit under 15 minutes."
                },
                {
                    "name": "Dynamic Automated Clearance Pricing",
                    "category": "Economics",
                    "importance": "High",
                    "ratings": {comp_names[0]: "no", comp_names[1]: "partial", comp_names[2]: "no"} if len(comp_names) >= 3 else {},
                    "reason": "Automatically reduces prices as closing time nears to maximize sell-through without manual sticker repricing."
                },
                {
                    "name": "Automated Non-Profit / Shelter Donation Routing",
                    "category": "Social Impact",
                    "importance": "High",
                    "ratings": {comp_names[0]: "no", comp_names[1]: "no", comp_names[2]: "no"} if len(comp_names) >= 3 else {},
                    "reason": "Zero major commercial platforms automatically dispatch verified tax-deductible donation pickups for unsold leftovers."
                }
            ]
        elif any(k in idea_lower for k in ["health", "triage", "senior", "clinic", "telehealth", "patient", "medical"]):
            features_def = [
                {
                    "name": "Vernacular Dialect Voice Agent",
                    "category": "Accessibility",
                    "importance": "Critical",
                    "ratings": {comp_names[0]: "no", comp_names[1]: "no", comp_names[2]: "partial"} if len(comp_names) >= 3 else {},
                    "reason": "Legacy telehealth portals demand English text typing on smartphones; a local voice agent unlocks elder adoption."
                },
                {
                    "name": "PSTN / Landline Voice Compatibility",
                    "category": "Connectivity",
                    "importance": "Critical",
                    "ratings": {comp_names[0]: "no", comp_names[1]: "no", comp_names[2]: "partial"} if len(comp_names) >= 3 else {},
                    "reason": "Operates over basic phone lines without requiring 4G data or smartphone apps."
                },
                {
                    "name": "Zero-Wait Emergency Symptom Stratification",
                    "category": "Clinical Reliability",
                    "importance": "High",
                    "ratings": {comp_names[0]: "partial", comp_names[1]: "partial", comp_names[2]: "no"} if len(comp_names) >= 3 else {},
                    "reason": "Instantly triages red-flag vitals without 30-minute call center queues."
                },
                {
                    "name": "Caregiver & Family SMS Escalation",
                    "category": "Communication",
                    "importance": "High",
                    "ratings": {comp_names[0]: "partial", comp_names[1]: "no", comp_names[2]: "no"} if len(comp_names) >= 3 else {},
                    "reason": "Immediately alerts remote family members with localized symptom summaries upon emergency detection."
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