from utils.llm import call_llm

def critique(text):
    prompt = f"Check for hallucinations or unsupported claims:\n{text}"
    return call_llm(prompt, max_tokens=500)