from sentence_transformers import SentenceTransformer
import numpy as np

_model = None

def embed(texts):
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return np.array(_model.encode(texts, normalize_embeddings=True), dtype="float32")
