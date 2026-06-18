from fastapi import APIRouter, HTTPException, Query

from app.models.skills import SkillSearchRequest, SkillStackRequest, SkillResult, SkillStackResult, SkillListResponse
from app.services.skills.engine import search, search_stack, list_domains, list_stacks

router = APIRouter(prefix="/api/skills", tags=["skills"])


@router.post("/search", response_model=SkillResult)
def search_skill(req: SkillSearchRequest):
    try:
        result = search(req.query, req.domain, req.max_results)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stack", response_model=SkillStackResult)
def search_skill_stack(req: SkillStackRequest):
    try:
        result = search_stack(req.query, req.stack, req.max_results)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/domains")
def get_domains():
    return {"domains": list_domains(), "stacks": list_stacks()}
