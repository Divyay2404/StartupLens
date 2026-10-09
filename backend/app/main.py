import os
import logging
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.models.schemas import IdeaInputRequest, OpportunityReport, ResearchPlan
from app.services.query_planner import QueryPlanner
from app.services.ai_engine import AIEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("StartupLens")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="StartupLens: AI-powered startup idea validation and opportunity discovery platform backed by SerpApi multi-engine live intelligence."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "serpapi_configured": bool(settings.SERPAPI_API_KEY and settings.SERPAPI_API_KEY.strip()),
        "gemini_configured": bool(settings.GEMINI_API_KEY and settings.GEMINI_API_KEY.strip()),
        "openai_configured": bool(settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.strip())
    }

@app.post("/api/plan", response_model=ResearchPlan)
def generate_research_plan(request: IdeaInputRequest):
    """
    Step 1: AI Query Planner
    Decomposes startup idea into targeted queries across Google Search, News, Scholar, Trends, Patents.
    """
    try:
        return QueryPlanner.plan(
            idea=request.idea,
            target_region=request.target_region or "Global",
            include_patents=request.include_patents
        )
    except Exception as e:
        logger.error(f"Error generating research plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze", response_model=OpportunityReport)
async def analyze_startup_idea(request: IdeaInputRequest):
    """
    Full Workflow:
    Idea -> Query Planner -> SerpApi Multi-Engine -> Evidence Engine ->
    Competitor Engine -> Opportunity Gap Engine -> Opportunity Report
    """
    try:
        logger.info(f"Analyzing startup idea: '{request.idea[:60]}...'")
        report = await AIEngine.analyze_idea(request)
        return report
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis pipeline error: {str(e)}")

@app.get("/api/examples")
def get_sample_ideas():
    return [
        {
            "id": "rural_attendance",
            "title": "AI Attendance System for Rural Schools",
            "tag": "EdTech & Computer Vision",
            "description": "An automated facial recognition attendance system optimized for low-connectivity rural schools with intermittent electricity and no high-speed internet.",
            "target_region": "Emerging Markets / Rural",
            "highlight": "Featured in Track 5 Brief"
        },
        {
            "id": "soil_health",
            "title": "Smartphone Soil Health Scanner for Smallholders",
            "tag": "AgriTech & Remote Sensing",
            "description": "Instant optical soil nutrient analysis using smartphone camera color calibration cards to diagnose NPK deficiencies without expensive laboratory spectrometers.",
            "target_region": "Global South / Agriculture",
            "highlight": "High Social Impact"
        },
        {
            "id": "bakery_surplus",
            "title": "Hyperlocal Bakery Surplus Real-Time Clearinghouse",
            "tag": "FoodTech & Circular Economy",
            "description": "B2B micro-marketplace that alerts neighborhood cafes and shelters to fresh unsold bakery goods 1 hour before closing with dynamic pricing.",
            "target_region": "Urban Centers",
            "highlight": "Micro-SaaS Niche"
        },
        {
            "id": "senior_triage",
            "title": "AI Voice Agent for Rural Senior Telehealth Triage",
            "tag": "HealthTech & Voice AI",
            "description": "Phone-call based voice assistant capable of triaging symptoms in local vernacular dialects for elderly patients who lack smartphones or internet literacy.",
            "target_region": "Rural Healthcare",
            "highlight": "Accessibility Wedge"
        }
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
