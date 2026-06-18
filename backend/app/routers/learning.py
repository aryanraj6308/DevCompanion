from fastapi import APIRouter, HTTPException

from app.models.chat import ChatRequest, ChatResponse
from app.services.tools.teacher import teach_concept, explain_error

router = APIRouter(prefix="/api/learn", tags=["learning"])


class TeachRequest(ChatRequest):
    level: str = "beginner"


class ErrorExplainRequest(ChatRequest):
    error: str = ""
    code_context: str = ""


@router.post("/teach")
def teach(req: TeachRequest):
    try:
        reply = teach_concept(req.message, level=req.level, provider=req.provider)
        return ChatResponse(session_id=req.session_id or "learn", reply=reply, tool="learn")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/explain-error")
def explain_error_endpoint(req: ErrorExplainRequest):
    try:
        reply = explain_error(req.error, req.code_context, provider=req.provider)
        return ChatResponse(session_id=req.session_id or "learn", reply=reply, tool="learn")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
