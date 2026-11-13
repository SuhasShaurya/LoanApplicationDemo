import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Configuration
    API_HOST = os.getenv("API_HOST", "127.0.0.1")
    API_PORT = int(os.getenv("API_PORT", 8000))

    # LLM Configuration - General
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "claude-sonnet-4-20250514")
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", 2000))

    # LLM Configuration - Reasoning Engine
    LLM_MODEL = os.getenv("LLM_MODEL", "claude-opus-4-1")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.7))
    LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", 2000))
    USE_LLM_REASONING = os.getenv("USE_LLM_REASONING", "true").lower() == "true"
    BORDERLINE_CONFIDENCE_THRESHOLD = float(os.getenv("BORDERLINE_CONFIDENCE_THRESHOLD", 0.6))
    LLM_THINKING_BUDGET = int(os.getenv("LLM_THINKING_BUDGET", 5000))

    # Streamlit Configuration
    STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", 8501))

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Decision Thresholds
    MIN_INCOME_STABILITY_SCORE = 0.5
    MAX_DEBT_TO_INCOME_RATIO = 0.5
    MIN_CREDIT_SCORE = 600
    MIN_CONFIDENCE_THRESHOLD = float(os.getenv("MIN_CONFIDENCE_THRESHOLD", 0.6))
    MANUAL_REVIEW_CONFIDENCE_THRESHOLD = float(os.getenv("MANUAL_REVIEW_CONFIDENCE_THRESHOLD", 0.6))

    # Retry Configuration
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))
    RETRY_DELAY = float(os.getenv("RETRY_DELAY", 1.0))

    # Orchestrator Configuration
    USE_ENHANCED_ORCHESTRATOR = os.getenv("USE_ENHANCED_ORCHESTRATOR", "true").lower() == "true"

settings = Settings()
