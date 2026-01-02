import requests
import hashlib
from bs4 import BeautifulSoup
from rag.schemas import Job
from urllib.parse import urljoin

BASE_URL = "https://www.indeed.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def fetch_jobs(limit=100, query="software engineer", location="Remote"):
    """
    Scrape Indeed job listings
    Note: Indeed actively blocks scrapers, so this may not always work
    Consider using their official API if available
    """
    jobs = []
    
    try:
        # Build search URL
        search_url = f"{BASE_URL}/jobs"
        params = {
            "q": query,
            "l": location,
            "sort": "date"
        }
        
        response = requests.get(search_url, headers=HEADERS, params=params, timeout=20)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Indeed's job cards (selector may change)
        job_cards = soup.find_all("div", class_="job_seen_beacon")
        
        for card in job_cards[:limit]:
            try:
                # Extract title
                title_elem = card.find("h2", class_="jobTitle")
                if not title_elem:
                    continue
                title = title_elem.get_text(strip=True)
                
                # Extract company
                company_elem = card.find("span", {"data-testid": "company-name"})
                company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                
                # Extract location
                location_elem = card.find("div", {"data-testid": "text-location"})
                job_location = location_elem.get_text(strip=True) if location_elem else "Remote"
                
                # Extract job link
                link_elem = title_elem.find("a")
                job_link = urljoin(BASE_URL, link_elem["href"]) if link_elem and link_elem.get("href") else ""
                
                # Extract snippet
                snippet_elem = card.find("div", class_="job-snippet")
                description = snippet_elem.get_text(strip=True) if snippet_elem else ""
                
                jid = hashlib.md5((title + company + job_link).encode()).hexdigest()[:12]
                
                jobs.append(Job(
                    job_id=jid,
                    title=title,
                    company=company,
                    location=job_location,
                    description=description,
                    tags=["indeed"],
                    url=job_link,
                    source="Indeed"
                ))
            except Exception as e:
                print(f"Error parsing Indeed job card: {e}")
                continue
        
    except Exception as e:
        print(f"Error fetching Indeed jobs: {e}")
    
    return jobs