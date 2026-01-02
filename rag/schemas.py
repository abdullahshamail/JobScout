from pydantic import BaseModel
from typing import List, Optional

class Job(BaseModel):
    job_id: str
    title: str
    company: str
    location: str
    description: str
    tags: List[str]
    url: str
    source: Optional[str] = "Unknown"

class JobMatch(BaseModel):
    job: Job
    score: float
    explanation: str
    gaps: List[str]
