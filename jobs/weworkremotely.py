import feedparser
import hashlib
from rag.schemas import Job

# Multiple category feeds; add more if you want
FEEDS = [
    "https://weworkremotely.com/categories/remote-programming-jobs.rss",
    "https://weworkremotely.com/categories/remote-data-jobs.rss",
    "https://weworkremotely.com/categories/remote-devops-sysadmin-jobs.rss",
]

def fetch_jobs(limit=200):
    jobs = []
    for feed_url in FEEDS:
        feed = feedparser.parse(feed_url)
        for e in feed.entries[:limit]:
            title = e.get("title", "")
            link = e.get("link", "")
            # WWR often puts company in title like "Company: Role"
            company = ""
            if ":" in title:
                parts = title.split(":", 1)
                company = parts[0].strip()
                title_clean = parts[1].strip()
            else:
                title_clean = title

            summary = e.get("summary", "") or e.get("description", "") or ""
            jid = hashlib.md5((title_clean + company + link).encode()).hexdigest()[:12]
            jobs.append(Job(
                job_id=jid,
                title=title_clean,
                company=company or "Unknown",
                location="Remote",
                description=summary,
                tags=[],
                url=link,
                source="WeWorkRemotely"
            ))
    return jobs
