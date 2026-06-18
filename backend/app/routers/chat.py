import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
import json

from app.db.database import get_db
from app.db.models import ChatMessage
from app.models.chat import ChatRequest, ChatResponse, HistoryRequest, HistoryResponse, Message
from app.services.llm.router import router as llm_router
from app.services.rag.engine import get_rag_engine

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    session_id = req.session_id or str(uuid.uuid4())

    db.add(ChatMessage(session_id=session_id, role="user", content=req.message, tool=req.tool or "chat"))
    db.commit()

    messages = []
    history = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at).limit(20).all()
    for msg in history:
        messages.append({"role": msg.role, "content": msg.content})

    rag_context = ""
    if req.context:
        rag_context = req.context
    else:
        try:
            engine = get_rag_engine()
            rag_context = engine.get_context(req.message)
        except Exception:
            rag_context = ""

    if rag_context:
        messages.insert(-1, {"role": "system", "content": f"Relevant project context:\n{rag_context}"})

    try:
        reply = llm_router.generate(messages, provider=req.provider, model=req.model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    db.add(ChatMessage(session_id=session_id, role="assistant", content=reply, tool=req.tool or "chat"))
    db.commit()

    return ChatResponse(session_id=session_id, reply=reply, tool=req.tool or "chat")


@router.post("/stream")
def chat_stream(req: ChatRequest, db: Session = Depends(get_db)):
    session_id = req.session_id or str(uuid.uuid4())

    db.add(ChatMessage(session_id=session_id, role="user", content=req.message, tool=req.tool or "chat"))
    db.commit()

    messages = []
    history = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at).limit(20).all()
    for msg in history:
        messages.append({"role": msg.role, "content": msg.content})

    rag_context = ""
    try:
        engine = get_rag_engine()
        rag_context = engine.get_context(req.message)
    except Exception:
        rag_context = ""

    if rag_context:
        messages.insert(-1, {"role": "system", "content": f"Relevant project context:\n{rag_context}"})

    async def generate():
        full_reply = ""
        try:
            for chunk in llm_router.generate_stream(messages, provider=req.provider, model=req.model):
                full_reply += chunk
                yield f"data: {json.dumps({'content': chunk})}\n\n"
            db.add(ChatMessage(session_id=session_id, role="assistant", content=full_reply, tool=req.tool or "chat"))
            db.commit()
            yield f"data: {json.dumps({'done': True, 'session_id': session_id})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.post("/history", response_model=HistoryResponse)
def get_history(req: HistoryRequest, db: Session = Depends(get_db)):
    rows = db.query(ChatMessage).filter(
        ChatMessage.session_id == req.session_id
    ).order_by(ChatMessage.created_at).limit(req.limit).all()
    return HistoryResponse(
        session_id=req.session_id,
        messages=[Message(role=r.role, content=r.content, tool=r.tool) for r in rows],
    )


@router.get("/providers")
def list_providers():
    return {"providers": llm_router.list_providers()}
