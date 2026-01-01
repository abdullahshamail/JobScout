import requests
import hashlib
from rag.schemas import Job

URL = "https://remoteok.com/api"

def fetch_jobs(limit=100):
    data = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30).json()[1:]
    jobs = []
    for j in data[:limit]:
        title = j.get("position", "")
        company = j.get("company", "")
        link = j.get("url") or j.get("apply_url") or "https://remoteok.com"
        jid = hashlib.md5((title + company + link).encode()).hexdigest()[:12]
        jobs.append(Job(
            job_id=jid,
            title=title,
            company=company,
            location=j.get("location", "Remote") or "Remote",
            description=j.get("description", "") or "",
            tags=j.get("tags", []) or [],
            url=link,
            source="RemoteOK"
        ))
    return jobs
