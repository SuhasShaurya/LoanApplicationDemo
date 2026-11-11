import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Configuration
    API_HOST = os.getenv("API_HOST", "127.0.0.1")
    API_PORT = int(os.getenv("API_PORT", 8000))

    # LLM Configuration
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "claude-sonnet-4-20250514")
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", 2000))

    # Streamlit Configuration
    STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", 8501))

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Decision Thresholds
    MIN_INCOME_STABILITY_SCORE = 0.5
    MAX_DEBT_TO_INCOME_RATIO = 0.5
    MIN_CREDIT_SCORE = 600
    MIN_CONFIDENCE_THRESHOLD = 0.6

settings = Settings()
