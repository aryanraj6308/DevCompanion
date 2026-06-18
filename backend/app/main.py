from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pathlib import Path
from app.db.database import init_db
from app.routers import chat, projects, rag, learning, skills
from app.services.rag.engine import get_rag_engine

app = FastAPI(
    title="Local AI Engineer",
    description="Personal AI Software Engineer Agent - runs locally with Ollama",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(projects.router)
app.include_router(rag.router)
app.include_router(learning.router)
app.include_router(skills.router)


@app.on_event("startup")
def on_startup():
    init_db()
    _index_skills_into_rag()


def _index_skills_into_rag():
    guidelines_file = Path(__file__).resolve().parent.parent / "data" / "skills" / "vercel-guidelines" / "guidelines.txt"
    if not guidelines_file.exists():
        return
    engine = get_rag_engine()
    content = guidelines_file.read_text(encoding="utf-8")
    engine.index(content, "vercel-web-interface-guidelines.txt", {"source": "vercel", "type": "design-guidelines"})


@app.get("/api/health")
def health():
    return {"status": "ok", "version": "1.0.0"}
