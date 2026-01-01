from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "storage"
DATA.mkdir(exist_ok=True)

FAISS_INDEX = DATA / "jobs.faiss"
META = DATA / "meta.npy"
