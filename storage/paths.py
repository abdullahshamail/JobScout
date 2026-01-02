from pathlib import Path

STORAGE_DIR = Path(__file__).parent
FAISS_INDEX = STORAGE_DIR / "jobs.faiss"  # Legacy, not used anymore
META = STORAGE_DIR / "meta.npy"  # Legacy, not used anymore

# Create storage directory if it doesn't exist
STORAGE_DIR.mkdir(exist_ok=True)