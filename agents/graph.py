from langgraph.graph import StateGraph
from agents.state import AgentState
from agents.planner_agent import planner_agent
from agents.match_agent import match_agent
from agents.tools import ingest_jobs, enrich_jobs
from agents.explainer import explain
from agents.critic import critique

# If you have a gap analysis function somewhere, keep this import.
# If you don't, comment it out or delete it.
try:
    from agents.gap_agent import gap_analysis  # optional
except Exception:
    gap_analysis = None


def ingest_node(state: AgentState) -> AgentState:
    # defensive
    if state.agent_log is None:
        state.agent_log = []

    state.agent_log.append(f"Ingest: fetching jobs from {state.use_sources}")
    state.jobs = ingest_jobs(state.use_sources)
    return state


def enrich_node(state: AgentState) -> AgentState:
    if state.agent_log is None:
        state.agent_log = []

    if state.fetch_descriptions:
        state.agent_log.append("Enrich: fetching full job descriptions")
        state.jobs = enrich_jobs(state.jobs)
    else:
        state.agent_log.append("Enrich: skipped")
    return state


def explain_node(state: AgentState) -> AgentState:
    if state.agent_log is None:
        state.agent_log = []

    if not state.matches:
        state.explanation = "No matches to explain."
        return state

    job, score = state.matches[0]
    state.explanation = explain(job, state.resume_text)
    state.agent_log.append(f"Explainer: explained top match (score={score:.3f})")
    return state


def critic_node(state: AgentState) -> AgentState:
    if state.agent_log is None:
        state.agent_log = []

    if not state.explanation:
        state.critique = "No explanation produced."
        return state

    state.agent_log.append("Critic: checking explanation for hallucinations")
    state.critique = critique(state.explanation)
    return state


def gap_node(state: AgentState) -> AgentState:
    # Optional: only run if you actually have gap_analysis implemented.
    if state.agent_log is None:
        state.agent_log = []

    if not getattr(state, "run_gap_analysis", False):
        return state

    if not state.matches:
        state.gap_analysis = "No matches available for gap analysis."
        return state

    if gap_analysis is None:
        state.gap_analysis = "Gap analysis not implemented (agents/gap.py missing)."
        return state

    job, _ = state.matches[0]
    state.gap_analysis = gap_analysis(job, state.resume_text)
    state.agent_log.append("GapAgent: analyzed missing skills")
    return state


graph = StateGraph(AgentState)

graph.add_node("planner", planner_agent)
graph.add_node("ingest", ingest_node)
graph.add_node("enrich", enrich_node)
graph.add_node("match", match_agent)
graph.add_node("gap", gap_node)
graph.add_node("explain", explain_node)
graph.add_node("critic", critic_node)

graph.set_entry_point("planner")
graph.add_edge("planner", "ingest")
graph.add_edge("ingest", "enrich")
graph.add_edge("enrich", "match")
graph.add_edge("match", "gap")
graph.add_edge("gap", "explain")
graph.add_edge("explain", "critic")

job_graph = graph.compile()
