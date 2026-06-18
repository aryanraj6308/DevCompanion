import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from app.db.database import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True)
    session_id = Column(String(64), index=True)
    role = Column(String(16))
    content = Column(Text)
    tool = Column(String(32), default="chat")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    description = Column(Text, default="")
    tech_stack = Column(JSON, default=list)
    folder_structure = Column(Text, default="")
    plan = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    filename = Column(String(256))
    content = Column(Text)
    doc_metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
