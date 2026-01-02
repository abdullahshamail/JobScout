import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
STORAGE_DIR = BASE_DIR / "storage"
STORAGE_DIR.mkdir(exist_ok=True)

# LLM Configuration - Use Groq (free cloud API)
USE_CLOUD_LLM = os.getenv("USE_CLOUD_LLM", "true").lower() == "true"
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-70b-versatile")  # Groq model
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.0"))

# Fallback to Ollama for local development
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = "llama3.1:8b"

# Embedding Configuration
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
EMBEDDING_DIM = 384

# Job Fetching Configuration
DEFAULT_JOB_LIMIT = int(os.getenv("DEFAULT_JOB_LIMIT", "100"))  # Reduced for cloud
FETCH_TIMEOUT = int(os.getenv("FETCH_TIMEOUT", "20"))

# Matching Configuration
DEFAULT_TOP_K = int(os.getenv("DEFAULT_TOP_K", "10"))
DEFAULT_RUN_GAP_ANALYSIS = os.getenv("DEFAULT_RUN_GAP_ANALYSIS", "true").lower() == "true"

# Storage paths
FAISS_INDEX_PATH = STORAGE_DIR / "jobs.faiss"
META_PATH = STORAGE_DIR / "meta.npy"
CACHE_DIR = STORAGE_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)

# API Configuration
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (AutoJobScout/1.0)"
}

# Deployment Configuration
IS_PRODUCTION = os.getenv("ENVIRONMENT", "development") == "production"
DEBUG_MODE = not IS_PRODUCTION

# Streamlit Configuration
STREAMLIT_PAGE_TITLE = "AutoJobScout - AI Job Discovery"
STREAMLIT_PAGE_ICON = "🧭"
STREAMLIT_LAYOUT = "wide"