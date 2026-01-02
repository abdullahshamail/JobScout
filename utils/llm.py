"""
LLM helper that works with both local Ollama and cloud APIs (Groq)
"""
import requests
import config

def call_llm(prompt: str, max_tokens: int = 1000) -> str:
    """
    Call LLM with automatic fallback between Groq (cloud) and Ollama (local)
    """
    if config.USE_CLOUD_LLM and config.GROQ_API_KEY:
        return _call_groq(prompt, max_tokens)
    else:
        return _call_ollama(prompt, max_tokens)


def _call_groq(prompt: str, max_tokens: int) -> str:
    """Call Groq API (free, fast cloud LLM)"""
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {config.GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": config.LLM_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": config.LLM_TEMPERATURE,
                "max_tokens": max_tokens
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Groq API error: {e}")
        return f"Error calling LLM: {str(e)}"


def _call_ollama(prompt: str, max_tokens: int) -> str:
    """Call local Ollama API"""
    try:
        response = requests.post(
            f"{config.OLLAMA_BASE_URL}/api/chat",
            json={
                "model": config.OLLAMA_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()
        return response.json()["message"]["content"]
    except Exception as e:
        print(f"Ollama error: {e}")
        return f"Error calling LLM: {str(e)}"