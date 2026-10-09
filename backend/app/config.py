import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    PROJECT_NAME: str = "StartupLens"
    VERSION: str = "1.0.0"
    SERPAPI_API_KEY: str = os.getenv("SERPAPI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MOCK_FALLBACK: bool = os.getenv("MOCK_FALLBACK", "true").lower() in ("true", "1", "yes")

settings = Settings()
