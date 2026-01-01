from rag.embeddings import embed

def match_jobs(index, resume_text, top_k=10):
    qvec = embed([resume_text])
    return index.search(qvec, top_k)
