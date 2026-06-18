from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    provider: Optional[str] = None
    model: Optional[str] = None
    tool: Optional[str] = "chat"
    context: Optional[str] = None


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    tool: str


class HistoryRequest(BaseModel):
    session_id: str
    limit: int = 50


class Message(BaseModel):
    role: str
    content: str
    tool: str = "chat"


class HistoryResponse(BaseModel):
    session_id: str
    messages: List[Message]
