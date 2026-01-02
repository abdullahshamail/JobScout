import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (AutoJobScout/1.0)"
}

def fetch_job_description(url, timeout=20, max_chars=6000):
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.raise_for_status()
    except Exception:
        return ""

    soup = BeautifulSoup(r.text, "html.parser")

    # Remove scripts/styles
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    text = " ".join(text.split())

    # Heuristic: job pages are long; keep middle chunk
    if len(text) > max_chars:
        text = text[:max_chars]

    return text
