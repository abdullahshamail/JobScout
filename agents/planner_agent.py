from utils.llm import call_llm
from pydantic import BaseModel, Field
from typing import List
import json

# ---------------- Schema ----------------
class PlannerOutput(BaseModel):
    use_sources: List[str] = Field(description="Job sources to query")
    fetch_descriptions: bool = Field(description="Whether to fetch full job descriptions")
    top_k: int = Field(description="Number of top jobs to return")
    run_gap_analysis: bool = Field(description="Whether to run skill gap analysis")

def planner_agent(state):
    if state.agent_log is None:
        state.agent_log = []

    prompt = f"""
You are a planner agent for a job discovery system.

Your job is to decide HOW the pipeline should run.

Given:
- A resume
- A job search intent

Choose from the following job sources ONLY:
RemoteOK, Remotive, WeWorkRemotely, NewGradJobs

Resume:
{state.resume_text[:2000]}

Intent:
{state.user_intent}

Return ONLY a JSON object with these fields:
- use_sources: array of source names
- fetch_descriptions: boolean
- top_k: number (5-20)
- run_gap_analysis: boolean

JSON output:
"""

    try:
        response = call_llm(prompt, max_tokens=300)
        
        # Extract JSON from response (handle markdown code blocks)
        json_str = response.strip()
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0]
        elif "```" in json_str:
            json_str = json_str.split("```")[1].split("```")[0]
        
        parsed = json.loads(json_str)
        plan = PlannerOutput(**parsed)
    except Exception as e:
        print(f"Planner parsing error: {e}")
        # Fallback to defaults
        plan = PlannerOutput(
            use_sources=["RemoteOK", "Remotive", "WeWorkRemotely"],
            fetch_descriptions=False,  # Faster for cloud
            top_k=10,
            run_gap_analysis=True
        )

    state.use_sources = plan.use_sources
    state.fetch_descriptions = plan.fetch_descriptions
    state.top_k = plan.top_k
    state.run_gap_analysis = plan.run_gap_analysis

    state.agent_log.append(
        f"Planner: sources={plan.use_sources}, "
        f"fetch_descriptions={plan.fetch_descriptions}, "
        f"top_k={plan.top_k}, "
        f"run_gap_analysis={plan.run_gap_analysis}"
    )
    return state