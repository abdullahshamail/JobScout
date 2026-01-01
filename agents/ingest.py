from rag.embeddings import embed
from rag.index import JobIndex
from jobs.remoteok import fetch_jobs as fetch_remoteok
from jobs.remotive import fetch_jobs as fetch_remotive
from jobs.weworkremotely import fetch_jobs as fetch_wwr

def ingest(job_limit_per_source=150):
    sources = [
        ("RemoteOK", lambda: fetch_remoteok(limit=job_limit_per_source)),
        ("Remotive", lambda: fetch_remotive(limit=job_limit_per_source)),
        ("WeWorkRemotely", lambda: fetch_wwr(limit=job_limit_per_source)),
    ]

    all_jobs = []
    for _, fn in sources:
        try:
            all_jobs.extend(fn())
        except Exception as e:
            # don’t crash whole pipeline if one source fails
            print(f"[WARN] source failed: {e}")

    # DEDUPE by URL (best), fallback by (title, company)
    seen = set()
    deduped = []
    for j in all_jobs:
        key = (j.url or "", j.title.lower(), j.company.lower())
        if key in seen:
            continue
        seen.add(key)
        deduped.append(j)

    # Build embeddings
    texts = [(j.title + " " + j.company + " " + j.location + " " + j.description) for j in deduped]
    vecs = embed(texts)

    idx = JobIndex()
    idx.add(vecs, deduped)
    return idx, len(all_jobs), len(deduped)
