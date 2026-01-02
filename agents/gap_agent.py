import requests

OLLAMA = "http://localhost:11434/api/chat"

def gap_analysis(job, resume):
    prompt = f"""
Resume:
{resume}

Job:
{job.title} at {job.company}

List:
1. Missing skills
2. Suggested resume improvements
Keep it concise.
"""
    r = requests.post(OLLAMA, json={
        "model": "llama3.1:8b",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }).json()

    return r["message"]["content"]
