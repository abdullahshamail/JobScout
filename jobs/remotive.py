import requests
import hashlib
from rag.schemas import Job

URL = "https://remotive.com/api/remote-jobs"

def fetch_jobs(limit=200, category=None):
    params = {}
    if category:
        params["category"] = category

    data = requests.get(URL, params=params, timeout=30).json()
    items = data.get("jobs", [])
    jobs = []
    for j in items[:limit]:
        title = j.get("title", "")
        company = j.get("company_name", "")
        link = j.get("url", "")
        jid = hashlib.md5((title + company + link).encode()).hexdigest()[:12]
        jobs.append(Job(
            job_id=jid,
            title=title,
            company=company,
            location=j.get("candidate_required_location", "Remote") or "Remote",
            description=j.get("description", "") or "",
            tags=j.get("tags", []) or [],
            url=link,
            source="Remotive"
        ))
    return jobs
