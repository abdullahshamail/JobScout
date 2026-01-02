from utils.llm import call_llm

def explain(job, resume):
    if isinstance(job, (list, tuple)):
        job = job[0]  # fail-safe

    prompt = f"""
Resume:
{resume[:3000]}

Job:
{job.title} at {job.company}
{job.description[:2000]}

Explain fit and missing skills in 3-4 sentences.
"""
    return call_llm(prompt, max_tokens=500)