from pathlib import Path

STORAGE_DIR = Path(__file__).parent
FAISS_INDEX = STORAGE_DIR / "jobs.faiss"
META = STORAGE_DIR / "meta.npy"

STORAGE_DIR.mkdir(exist_ok=True)
