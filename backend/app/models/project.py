from pydantic import BaseModel
from typing import List, Optional


class ProjectRequest(BaseModel):
    name: str
    description: Optional[str] = ""
    tech_stack: Optional[List[str]] = None


class ArchitectureRequest(BaseModel):
    project_name: str
    description: str
    tech_stack: Optional[List[str]] = None


class ArchitectureResponse(BaseModel):
    plan: str
    folder_structure: str
    tech_stack: List[str]
    recommendations: str


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    tech_stack: List[str]
    plan: str
    created_at: str
