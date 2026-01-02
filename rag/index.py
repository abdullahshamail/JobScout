import faiss
import numpy as np
from storage.paths import FAISS_INDEX, META

class JobIndex:
    def __init__(self, dim=384):
        self.index = faiss.IndexFlatIP(dim)
        self.meta = []

        if FAISS_INDEX.exists():
            self.index = faiss.read_index(str(FAISS_INDEX))
            self.meta = list(np.load(str(META), allow_pickle=True))

    def add(self, vectors, jobs):
        self.index.add(vectors)
        self.meta.extend(jobs)
        faiss.write_index(self.index, str(FAISS_INDEX))
        np.save(str(META), np.array(self.meta, dtype=object), allow_pickle=True)

    def search(self, qvec, top_k: int):
        # returns indices + scores
        scores, idxs = self.index.search(qvec, top_k)

        out = []
        for score, idx in zip(scores[0], idxs[0]):
            if idx == -1:
                continue
            job = self.meta[idx]   # or however you store jobs
            out.append((job, float(score)))
        return out

