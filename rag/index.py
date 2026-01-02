import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from pathlib import Path
from storage.paths import STORAGE_DIR

META_FILE = STORAGE_DIR / "meta.pkl"
VECTORS_FILE = STORAGE_DIR / "vectors.npy"

class JobIndex:
    def __init__(self):
        self.vectors = None
        self.meta = []
        
        # Load existing index if available
        if META_FILE.exists() and VECTORS_FILE.exists():
            try:
                with open(META_FILE, 'rb') as f:
                    self.meta = pickle.load(f)
                self.vectors = np.load(VECTORS_FILE)
            except Exception as e:
                print(f"Failed to load index: {e}")
                self.vectors = None
                self.meta = []

    def add(self, vectors, jobs):
        """Add vectors and job metadata to the index"""
        if self.vectors is None:
            self.vectors = vectors
        else:
            self.vectors = np.vstack([self.vectors, vectors])
        
        self.meta.extend(jobs)
        
        # Save to disk
        try:
            STORAGE_DIR.mkdir(parents=True, exist_ok=True)
            with open(META_FILE, 'wb') as f:
                pickle.dump(self.meta, f)
            np.save(VECTORS_FILE, self.vectors)
        except Exception as e:
            print(f"Failed to save index: {e}")

    def search(self, qvec, top_k: int):
        """Search for top_k most similar jobs using cosine similarity"""
        if self.vectors is None or len(self.meta) == 0:
            return []
        
        # Ensure qvec is 2D
        if qvec.ndim == 1:
            qvec = qvec.reshape(1, -1)
        
        # Compute cosine similarity
        similarities = cosine_similarity(qvec, self.vectors)[0]
        
        # Get top k indices
        top_k = min(top_k, len(similarities))
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Return (job, score) tuples
        results = []
        for idx in top_indices:
            if idx < len(self.meta):
                job = self.meta[idx]
                score = float(similarities[idx])
                results.append((job, score))
        
        return results