from pydantic import BaseModel
from typing import List, Optional


class SkillSearchRequest(BaseModel):
    query: str
    domain: Optional[str] = None
    max_results: int = 5


class SkillStackRequest(BaseModel):
    query: str
    stack: str
    max_results: int = 5


class SkillResult(BaseModel):
    domain: str
    query: str
    file: str
    count: int
    results: List[dict]


class SkillStackResult(BaseModel):
    domain: str
    stack: str
    query: str
    file: str
    count: int
    results: List[dict]


class SkillListResponse(BaseModel):
    domains: List[str]
    stacks: List[str]
