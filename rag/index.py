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

    def search(self, qvec, k=5):
        scores, idxs = self.index.search(qvec, k)
        return [(self.meta[i], scores[0][j]) for j, i in enumerate(idxs[0])]
