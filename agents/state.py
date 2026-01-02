from typing import List, Optional, Annotated, Dict, Any
from pydantic import BaseModel

def keep_first(a, b):
    return a if a else b

class AgentState(BaseModel):
    resume_text: Annotated[str, keep_first]
    user_intent: Annotated[str, keep_first]

    use_sources: List[str] = []
    fetch_descriptions: bool = True
    top_k: int = 10
    run_gap_analysis: bool = True

    jobs: list = []
    matches: list = []

    explanation: Optional[str] = None
    critique: Optional[str] = None
    gap_analysis: Optional[str] = None

    agent_log: List[str] = []

    agents: Dict[str, Dict[str, Any]] = {
        "state": {}
    }
