from jobs.remoteok import fetch_jobs as remoteok
from jobs.remotive import fetch_jobs as remotive
from jobs.weworkremotely import fetch_jobs as wwr
from jobs.newgrad_jobs import fetch_jobs as newgrad
from jobs.indeed import fetch_jobs as indeed
from jobs.adzuna import fetch_jobs as adzuna
from jobs.greenhouse import fetch_jobs as greenhouse
from agents.enrich import fetch_job_description

SOURCE_MAP = {
    "RemoteOK": remoteok,
    "Remotive": remotive,
    "WeWorkRemotely": wwr,
    "NewGradJobs": newgrad,
    "Indeed": indeed,
    "Adzuna": adzuna,
    "Greenhouse": greenhouse,
}

def ingest_jobs(sources, limit=150):
    """
    Fetch jobs from multiple sources
    
    Args:
        sources: List of source names (e.g., ['RemoteOK', 'Remotive'])
        limit: Max jobs per source
    
    Returns:
        List of Job objects
    """
    jobs = []
    for s in sources:
        if s in SOURCE_MAP:
            try:
                print(f"Fetching from {s}...")
                source_jobs = SOURCE_MAP[s](limit=limit)
                jobs.extend(source_jobs)
                print(f"✓ Fetched {len(source_jobs)} jobs from {s}")
            except Exception as e:
                print(f"✗ Failed to fetch from {s}: {e}")
        else:
            print(f"Warning: Unknown source '{s}'")
    
    return jobs

def enrich_jobs(jobs):
    """
    Fetch full job descriptions for jobs with short descriptions
    
    Args:
        jobs: List of Job objects
    
    Returns:
        List of Job objects with enriched descriptions
    """
    enriched = []
    for j in jobs:
        if not j.description or len(j.description) < 200:
            try:
                full_desc = fetch_job_description(j.url)
                if full_desc:
                    j.description = full_desc
            except Exception as e:
                print(f"Failed to enrich job {j.job_id}: {e}")
        enriched.append(j)
    return enriched