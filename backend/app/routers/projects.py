from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import json

from app.db.database import get_db
from app.db.models import Project
from app.models.project import ProjectRequest, ArchitectureRequest, ArchitectureResponse, ProjectResponse
from app.services.tools.project_planner import create_plan, generate_folder_structure

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.post("")
def create_project(req: ProjectRequest, db: Session = Depends(get_db)):
    project = Project(
        name=req.name,
        description=req.description,
        tech_stack=req.tech_stack or [],
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "tech_stack": project.tech_stack,
    }


@router.post("/architect", response_model=ArchitectureResponse)
def architect_project(req: ArchitectureRequest, provider: str = None):
    plan = create_plan(req.project_name, req.description, req.tech_stack, provider=provider)
    structure = generate_folder_structure(req.project_name, req.tech_stack, provider=provider)
    return ArchitectureResponse(
        plan=plan,
        folder_structure=structure,
        tech_stack=req.tech_stack or [],
        recommendations="Consider using the suggested architecture for optimal maintainability.",
    )


@router.get("")
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).order_by(Project.created_at.desc()).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "tech_stack": p.tech_stack,
            "created_at": p.created_at.isoformat() if p.created_at else "",
        }
        for p in projects
    ]


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectResponse(
        id=p.id,
        name=p.name,
        description=p.description,
        tech_stack=p.tech_stack or [],
        plan=p.plan or "",
        created_at=p.created_at.isoformat() if p.created_at else "",
    )


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(p)
    db.commit()
    return {"ok": True}
