from agents.state import AgentState
from rag.embeddings import embed
from rag.index import JobIndex


def _normalize_matches(raw):
    """
    raw could be:
      - [(job, score), ...] already
      - [((job, score), ...)] depending on index impl
    We normalize to: List[Tuple[job, float]]
    """
    if not raw:
        return []

    # If it's already list of tuples (job, score)
    first = raw[0]
    if isinstance(first, tuple) and len(first) == 2:
        return raw

    # Otherwise, try best-effort normalization
    norm = []
    for item in raw:
        if isinstance(item, tuple) and len(item) == 2:
            norm.append(item)
    return norm


def match_agent(state: AgentState) -> AgentState:
    if state.agent_log is None:
        state.agent_log = []

    if not state.jobs:
        state.matches = []
        state.agent_log.append("Match: no jobs to rank")
        return state

    index = JobIndex()

    texts = []
    for j in state.jobs:
        title = getattr(j, "title", "") or ""
        company = getattr(j, "company", "") or ""
        desc = getattr(j, "description", "") or ""
        texts.append(f"{title} {company} {desc}")

    vecs = embed(texts)
    index.add(vecs, state.jobs)

    qvec = embed([state.resume_text])
    raw = index.search(qvec, state.top_k)

    state.matches = _normalize_matches(raw)
    state.agent_log.append(
        f"Match: embedded {len(state.jobs)} jobs and ranked against resume (top_k={state.top_k})"
    )
    return state
