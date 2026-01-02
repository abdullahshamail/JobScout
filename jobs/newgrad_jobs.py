import requests
import hashlib
from bs4 import BeautifulSoup
from rag.schemas import Job

BASE_URL = "https://www.newgrad-jobs.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; AutoJobScout/1.0)"
}

def fetch_jobs(limit=200):
    """
    Fetch job postings from newgrad-jobs.com
    Returns a list of Job objects
    """
    resp = requests.get(BASE_URL, headers=HEADERS, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    jobs = []

    # This selector may evolve — keep it isolated here
    job_cards = soup.select("a")  # site is mostly link-driven

    for a in job_cards:
        href = a.get("href", "")
        text = a.get_text(strip=True)

        # Heuristic: skip nav / empty links
        if not href or not text:
            continue

        # Only keep outbound job links
        if not href.startswith("http"):
            continue

        title = text
        company = "Unknown"

        # Try to infer company from title like "Company - Role"
        if " - " in title:
            parts = title.split(" - ", 1)
            company = parts[0].strip()
            title = parts[1].strip()

        jid = hashlib.md5((title + company + href).encode()).hexdigest()[:12]

        jobs.append(Job(
            job_id=jid,
            title=title,
            company=company,
            location="Unknown",
            description="",          # newgrad-jobs is link-heavy, not text-heavy
            tags=["new-grad"],
            url=href,
            source="NewGradJobs"
        ))

        if len(jobs) >= limit:
            break

    return jobs
