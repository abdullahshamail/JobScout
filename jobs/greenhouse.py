import requests
import hashlib
from rag.schemas import Job

# Greenhouse job boards are company-specific
# This is a generic aggregator approach
GREENHOUSE_BOARDS = [
    "https://boards-api.greenhouse.io/v1/boards/airbnb/jobs",
    "https://boards-api.greenhouse.io/v1/boards/gitlab/jobs",
    "https://boards-api.greenhouse.io/v1/boards/stripe/jobs",
    "https://boards-api.greenhouse.io/v1/boards/spotify/jobs",
    "https://boards-api.greenhouse.io/v1/boards/dropbox/jobs",
]

def fetch_jobs(limit=100):
    """
    Fetch jobs from Greenhouse-hosted job boards
    Note: This fetches from specific companies using Greenhouse
    """
    jobs = []
    
    for board_url in GREENHOUSE_BOARDS:
        if len(jobs) >= limit:
            break
        
        try:
            response = requests.get(board_url, timeout=20)
            response.raise_for_status()
            
            data = response.json()
            job_listings = data.get("jobs", [])
            
            for job_data in job_listings:
                if len(jobs) >= limit:
                    break
                
                title = job_data.get("title", "")
                company = board_url.split("/")[-2].capitalize()  # Extract company name
                location = job_data.get("location", {}).get("name", "Remote")
                url = job_data.get("absolute_url", "")
                
                # Get job description from details endpoint
                description = ""
                job_id_gh = job_data.get("id")
                if job_id_gh:
                    try:
                        detail_url = f"{board_url}/{job_id_gh}"
                        detail_resp = requests.get(detail_url, timeout=10)
                        detail_data = detail_resp.json()
                        description = detail_data.get("content", "")
                    except:
                        pass
                
                jid = hashlib.md5((title + company + url).encode()).hexdigest()[:12]
                
                jobs.append(Job(
                    job_id=jid,
                    title=title,
                    company=company,
                    location=location,
                    description=description,
                    tags=["greenhouse"],
                    url=url,
                    source="Greenhouse"
                ))
        
        except Exception as e:
            print(f"Error fetching from {board_url}: {e}")
            continue
    
    return jobs