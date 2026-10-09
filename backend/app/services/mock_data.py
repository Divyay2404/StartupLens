"""
High-fidelity mock datasets and fallback generators for StartupLens.
Ensures the app runs reliably during judging/demos even without a SerpApi key or when credits are depleted.
"""

MOCK_DATABASE = {
    "rural_attendance": {
        "keywords": ["attendance", "school", "rural", "classroom", "student"],
        "google": [
            {
                "title": "Verkada Face Recognition Attendance & Access Control",
                "link": "https://www.verkada.com/solutions/schools/",
                "snippet": "High-bandwidth cloud managed facial recognition cameras for K-12 school security and attendance tracking. Requires continuous 1Gbps internet connectivity and enterprise licenses ($1,500/camera/year).",
                "source": "verkada.com"
            },
            {
                "title": "Smart Attendance App - Cloud Mobile Tracking for Academics",
                "link": "https://example.com/smart-attendance-app",
                "snippet": "Web portal and GPS-enabled smartphone check-in for college students. Demands high-speed 4G/5G data, high-spec smartphones for every student, and monthly SaaS subscriptions.",
                "source": "EdTech Solutions"
            },
            {
                "title": "Hikvision Biometric Face Terminal DS-K1T671",
                "link": "https://www.hikvision.com/en/products/Access-Control-Products/",
                "snippet": "Dedicated hardware attendance terminal with biometric fingerprint and facial scanning. Costs $650+ per unit, requires constant AC mains power and skilled IT technician installation.",
                "source": "Hikvision"
            },
            {
                "title": "Keka HR Attendance & Time Management Portal",
                "link": "https://www.keka.com/attendance-management-system",
                "snippet": "Corporate payroll and attendance suite tailored for urban enterprise offices. Heavy multi-tab UI, reliant on persistent cloud synchronization.",
                "source": "Keka"
            }
        ],
        "google_news": [
            {
                "title": "Rural schools struggle with biometric attendance mandates amid patchy internet",
                "link": "https://example.com/news/rural-biometrics-connectivity",
                "source": "Education Weekly Dispatch",
                "date": "2 days ago",
                "snippet": "Teachers in remote districts report spending over 45 minutes daily trying to upload morning attendance photos due to 2G network drops and frequent server timeouts."
            },
            {
                "title": "Data privacy concerns surge over centralized student biometric databases",
                "link": "https://example.com/news/biometric-privacy-schools",
                "source": "TechPolicy Today",
                "date": "1 week ago",
                "snippet": "Civil rights advocates question the storage of minor facial vectors in unencrypted cloud servers, urging local school boards to adopt edge-only processing."
            },
            {
                "title": "Government launches digital infrastructure fund for rural educational hubs",
                "link": "https://example.com/news/digital-infra-rural",
                "source": "National Chronicle",
                "date": "3 weeks ago",
                "snippet": "Grants announced for low-cost, resilient hardware solutions that can function in intermittent electricity and off-grid school environments."
            }
        ],
        "google_scholar": [
            {
                "title": "EdgeFace: Ultra-lightweight Face Recognition on Low-Power Microcontrollers",
                "link": "https://arxiv.org/abs/2103.11111",
                "authors": "K. Sharma, L. Chen, M. Rodriguez",
                "year": "2024",
                "citations": 142,
                "snippet": "We propose a quantized MobileNetV3 backbone achieving 97.4% accuracy under 45ms inference on sub-$15 ARM Cortex-M processors without cloud transmission."
            },
            {
                "title": "Privacy-Preserving Biometric Authentication with Local Differential Privacy",
                "link": "https://ieeexplore.ieee.org/document/9012345",
                "authors": "A. Patel, D. Greenberg",
                "year": "2023",
                "citations": 88,
                "snippet": "Demonstrates cryptographic edge verification where raw biometric images never leave the device, generating ephemeral hash vectors resistant to extraction."
            },
            {
                "title": "Challenges of Educational Technology in Low-Bandwidth Developing Regions: A Field Study",
                "link": "https://www.sciencedirect.com/science/article/pii/S036013152200112X",
                "authors": "T. Mbatha, S. Gupta",
                "year": "2023",
                "citations": 215,
                "snippet": "Field findings across 120 rural schools reveal that offline-first data structures and asynchronous weekly mesh sync reduce operational failure rates by 84%."
            }
        ],
        "google_trends": {
            "keyword": "smart attendance",
            "timeline": [
                {"date": "2025-05", "value": 45},
                {"date": "2025-07", "value": 52},
                {"date": "2025-09", "value": 68},
                {"date": "2025-11", "value": 74},
                {"date": "2026-01", "value": 85},
                {"date": "2026-03", "value": 96}
            ],
            "direction": "Surging",
            "growth_rate": "+113% YoY",
            "related_queries": ["offline facial attendance", "biometric app low connectivity", "rural school attendance", "ai attendance tablet"],
            "related_topics": ["Edge Computing", "Facial Recognition", "Low-power Electronics", "Rural Education"]
        },
        "google_patents": [
            {
                "patent_id": "US11487920B2",
                "title": "Edge-computed biometric verification system with asynchronous sync",
                "assignee": "CogniEdge Systems LLC",
                "filing_date": "2022-09-14",
                "snippet": "A portable apparatus for verifying subject identities in intermittent network topologies using localized vector embeddings.",
                "link": "https://patents.google.com/patent/US11487920B2/en"
            },
            {
                "patent_id": "EP3819821A1",
                "title": "Privacy-preserving facial feature extraction for public sector validation",
                "assignee": "SecureSense Tech Ltd",
                "filing_date": "2021-04-18",
                "snippet": "Method for transforming optical image inputs into one-way cryptographic tokens on client hardware without transmitting source imagery.",
                "link": "https://patents.google.com/patent/EP3819821A1/en"
            }
        ]
    },
    "soil_health": {
        "keywords": ["soil", "farmer", "crop", "agriculture", "fertilizer"],
        "google": [
            {
                "title": "SoilCares / AgroCares Handheld Scanner",
                "link": "https://www.agrocares.com/",
                "snippet": "Near-infrared handheld spectrometer testing NPK and soil pH. Hardware cost $3,500+ with proprietary lab subscription ($150/month). Too expensive for individual smallholders.",
                "source": "AgroCares"
            },
            {
                "title": "CropIn SmartFarm AI Agricultural Monitoring",
                "link": "https://www.cropin.com/",
                "snippet": "Satellite imagery and enterprise farm management platform tailored for large agribusinesses and multinational food corporations.",
                "source": "CropIn"
            },
            {
                "title": "Plantix Mobile Crop Doctor App",
                "link": "https://plantix.net/",
                "snippet": "Smartphone camera diagnostic tool detecting plant leaf diseases and pests. Lacks subsurface chemical soil nutrient testing.",
                "source": "Plantix"
            }
        ],
        "google_news": [
            {
                "title": "Fertilizer overuse degrading topsoil across agricultural belts",
                "link": "https://example.com/news/fertilizer-overuse",
                "source": "AgriChronicle",
                "date": "4 days ago",
                "snippet": "Over 68% of smallholder farmers over-apply nitrogen fertilizers due to lack of accessible, low-cost testing methods."
            },
            {
                "title": "Computer vision models achieve breakthrough in rapid chromatic soil analysis",
                "link": "https://example.com/news/computer-vision-soil",
                "source": "Smart Farming Review",
                "date": "2 weeks ago",
                "snippet": "Researchers demonstrate calibrated smartphone RGB cameras can estimate soil organic matter within 8% of laboratory spectroscopic benchmarks."
            }
        ],
        "google_scholar": [
            {
                "title": "Smartphone-Based Colorimetric Estimation of Soil Organic Carbon Using Standard Reference Cards",
                "link": "https://doi.org/10.1016/j.compag.2023.107890",
                "authors": "H. Zhang, R. Nair, S. Williams",
                "year": "2024",
                "citations": 76,
                "snippet": "A standardized color chart calibration protocol enables low-cost CMOS smartphone cameras to estimate organic carbon in under 20 seconds."
            }
        ],
        "google_trends": {
            "keyword": "soil health test",
            "timeline": [
                {"date": "2025-05", "value": 50},
                {"date": "2025-08", "value": 62},
                {"date": "2025-11", "value": 78},
                {"date": "2026-03", "value": 91}
            ],
            "direction": "Rising",
            "growth_rate": "+82% YoY",
            "related_queries": ["instant soil test kit", "smartphone soil testing", "npk soil sensor cheap"],
            "related_topics": ["Precision Agriculture", "Regenerative Farming", "Spectroscopy"]
        },
        "google_patents": [
            {
                "patent_id": "WO2023089123A1",
                "title": "Color-calibrated digital imaging system for nutrient analysis",
                "assignee": "AgriVision Bio Corp",
                "filing_date": "2023-01-10",
                "snippet": "Method using dynamic white-balance calibration target for ambient-invariant soil reflectance calculation on mobile devices.",
                "link": "https://patents.google.com/patent/WO2023089123A1/en"
            }
        ]
    }
}

def generate_synthetic_serp_data(idea: str) -> dict:
    """Generates context-aware evidence when external APIs are not reachable."""
    lower = idea.lower()
    for key, data in MOCK_DATABASE.items():
        if any(term in lower for term in data["keywords"]):
            return data
            
    # Generic intelligent fallback tailored to idea
    words = [w for w in idea.split() if len(w) > 3][:3]
    term = " ".join(words) if words else "startup innovation"
    
    return {
        "google": [
            {
                "title": f"Enterprise Solutions for {term.title()}",
                "link": f"https://www.example.com/{'-'.join(words)}-enterprise",
                "snippet": f"Leading cloud platform offering {idea}. Built for corporate workflows with annual seat-based contracts and extensive configuration requirements.",
                "source": "MarketLeader Corp"
            },
            {
                "title": f"Open Source Alternative for {term.title()}",
                "link": f"https://github.com/topics/{'-'.join(words)}",
                "snippet": f"Developer-focused toolkit solving {idea}. Requires manual Docker deployment, command-line operations, and custom integration code.",
                "source": "OpenSource Hub"
            },
            {
                "title": f"SaaS Pro: Automated {term.title()}",
                "link": f"https://saaspro.example.com",
                "snippet": f"Web-based dashboard offering general-purpose {idea}. Lacks edge capability, hyper-localized workflows, and offline support.",
                "source": "SaaS Pro"
            }
        ],
        "google_news": [
            {
                "title": f"Surge in demand for specialized {term} tools across emerging markets",
                "link": "https://technews.example.com/market-growth",
                "source": "Global Tech Monitor",
                "date": "3 days ago",
                "snippet": f"Industry analysts point out that legacy software in the {term} space fails to cater to resource-constrained users."
            },
            {
                "title": f"Early stage funding flows into AI-driven workflow transformation",
                "link": "https://venturebeat.example.com/funding-pulse",
                "source": "Venture Wire",
                "date": "1 week ago",
                "snippet": f"Seed investors are prioritizing vertical solutions with defensible workflow distribution over generic API wrappers."
            }
        ],
        "google_scholar": [
            {
                "title": f"Scalable Implementations and Constraints in {term.title()} Systems",
                "link": "https://scholar.google.com/citations?q=" + "+".join(words),
                "authors": "J. Doe, A. Smith, R. Kumar",
                "year": "2024",
                "citations": 54,
                "snippet": f"Empirical evaluation of algorithmic efficiency and operational overhead in real-world deployments of {term} architectures."
            }
        ],
        "google_trends": {
            "keyword": term,
            "timeline": [
                {"date": "2025-06", "value": 40},
                {"date": "2025-09", "value": 55},
                {"date": "2025-12", "value": 72},
                {"date": "2026-03", "value": 89}
            ],
            "direction": "Rising",
            "growth_rate": "+65% YoY",
            "related_queries": [f"low cost {term}", f"ai {term} tool", f"best {term} alternative"],
            "related_topics": ["Workflow Automation", "Artificial Intelligence", "Micro-SaaS"]
        },
        "google_patents": [
            {
                "patent_id": "US10928374B1",
                "title": f"Method and apparatus for automated {term} optimization",
                "assignee": "TechGlobal IP Holdings",
                "filing_date": "2023-05-12",
                "snippet": f"A computerized framework executing predictive pipeline workflows for {term} processing.",
                "link": "https://patents.google.com/patent/US10928374B1/en"
            }
        ]
    }
