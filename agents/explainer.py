import requests

OLLAMA = "http://localhost:11434/api/chat"

def explain(job, resume):
    prompt = f"""
Resume:
{resume}

Job:
{job.title} at {job.company}
{job.description}

Explain fit and missing skills.
"""
    r = requests.post(OLLAMA, json={
        "model": "llama3.1:8b",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }).json()
    return r["message"]["content"]
