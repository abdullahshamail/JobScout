import requests

def critique(text):
    prompt = f"Check for hallucinations or unsupported claims:\n{text}"
    r = requests.post("http://localhost:11434/api/chat", json={
        "model": "llama3.1:8b",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }).json()
    return r["message"]["content"]
