from utils.llm import call_llm

def gap_analysis(job, resume):
    prompt = f"""
Resume:
{resume[:3000]}

Job:
{job.title} at {job.company}

List:
1. Missing skills
2. Suggested resume improvements
Keep it concise.
"""
    return call_llm(prompt, max_tokens=800)