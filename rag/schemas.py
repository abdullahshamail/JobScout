from pydantic import BaseModel
from typing import List, Dict

class Job(BaseModel):
    job_id: str
    title: str
    company: str
    location: str
    description: str
    tags: List[str]
    url: str
    source: str

class JobMatch(BaseModel):
    job: Job
    score: float
    explanation: str
    gaps: List[str]
