from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List

# ---------------- Schema ----------------
class PlannerOutput(BaseModel):
    use_sources: List[str] = Field(description="Job sources to query")
    fetch_descriptions: bool = Field(description="Whether to fetch full job descriptions")
    top_k: int = Field(description="Number of top jobs to return")
    run_gap_analysis: bool = Field(description="Whether to run skill gap analysis")

# ---------------- LLM ----------------
llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0.0
)

parser = JsonOutputParser(pydantic_object=PlannerOutput)

PROMPT = ChatPromptTemplate.from_template("""
You are a planner agent for a job discovery system.

Your job is to decide HOW the pipeline should run.

Given:
- A resume
- A job search intent

Choose from the following job sources ONLY:
RemoteOK, Remotive, WeWorkRemotely, NewGradJobs

Rules:
- Return ONLY valid JSON
- Do not include explanations
- Do not include markdown
- Do not include extra text

{format_instructions}

Resume:
{resume}

Intent:
{intent}
""")

def planner_agent(state):
    if state.agent_log is None:
        state.agent_log = []

    messages = PROMPT.format_messages(
        resume=state.resume_text[:2000],
        intent=state.user_intent,
        format_instructions=parser.get_format_instructions()
    )

    result = llm.invoke(messages)

    try:
        parsed = parser.parse(result.content)     # dict
        plan = PlannerOutput(**parsed)            # pydantic
    except Exception:
        plan = PlannerOutput(
            use_sources=["RemoteOK", "Remotive", "WeWorkRemotely"],
            fetch_descriptions=True,
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
