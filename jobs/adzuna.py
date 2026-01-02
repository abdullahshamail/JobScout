import requests
import hashlib
from rag.schemas import Job
import os

# Get free API keys from https://developer.adzuna.com/
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID", "")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY", "")

BASE_URL = "https://api.adzuna.com/v1/api/jobs"

def fetch_jobs(limit=100, country="us", query="software engineer"):
    """
    Fetch jobs from Adzuna API
    Free tier: 250 calls/month
    Signup: https://developer.adzuna.com/
    """
    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        print("Warning: Adzuna API credentials not set. Skipping Adzuna.")
        return []
    
    jobs = []
    
    try:
        url = f"{BASE_URL}/{country}/search/1"
        params = {
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_APP_KEY,
            "results_per_page": min(limit, 50),  # Max 50 per page
            "what": query,
            "where": "remote",
            "sort_by": "date"
        }
        
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        
        data = response.json()
        
        for job_data in data.get("results", [])[:limit]:
            title = job_data.get("title", "")
            company = job_data.get("company", {}).get("display_name", "Unknown")
            location = job_data.get("location", {}).get("display_name", "Remote")
            description = job_data.get("description", "")
            url = job_data.get("redirect_url", "")
            
            jid = hashlib.md5((title + company + url).encode()).hexdigest()[:12]
            
            jobs.append(Job(
                job_id=jid,
                title=title,
                company=company,
                location=location,
                description=description,
                tags=["adzuna"],
                url=url,
                source="Adzuna"
            ))
    
    except Exception as e:
        print(f"Error fetching Adzuna jobs: {e}")
    
    return jobs