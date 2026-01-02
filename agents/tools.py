from jobs.remoteok import fetch_jobs as remoteok
from jobs.remotive import fetch_jobs as remotive
from jobs.weworkremotely import fetch_jobs as wwr
from jobs.newgrad_jobs import fetch_jobs as newgrad
from agents.enrich import fetch_job_description

SOURCE_MAP = {
    "RemoteOK": remoteok,
    "Remotive": remotive,
    "WeWorkRemotely": wwr,
    "NewGradJobs": newgrad,
}

def ingest_jobs(sources, limit=150):
    jobs = []
    for s in sources:
        if s in SOURCE_MAP:
            jobs.extend(SOURCE_MAP[s](limit=limit))
    return jobs

def enrich_jobs(jobs):
    for j in jobs:
        if not j.description or len(j.description) < 200:
            j.description = fetch_job_description(j.url)
    return jobs
