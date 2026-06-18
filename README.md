# Local AI Engineer

A free, local-first Personal AI Software Engineer Agent. Runs entirely on your machine using Ollama for LLM inference and ChromaDB for RAG.

## Features

- **AI Coding Assistant** — Generate, explain, debug, and refactor code
- **Project Architect** — Design architectures, plan projects, suggest tech stacks
- **RAG Memory System** — Index your project files and query them
- **Learning Mode** — Learn programming concepts and understand errors

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | React + Vite + TailwindCSS |
| Backend | FastAPI (Python) |
| Database | SQLite |
| Vector DB | ChromaDB |
| Embeddings | all-MiniLM-L6-v2 (local) |
| LLM | Ollama (Qwen, DeepSeek, Llama, etc.) |
| Optional LLM | Groq API (free tier available) |

## Prerequisites

- Python 3.10+
- Node.js 18+
- [Ollama](https://ollama.com) installed

## Quick Start

```bash
# 1. Install Ollama and pull a model
ollama pull qwen2.5:7b

# 2. Install backend dependencies
cd backend
pip install -r requirements.txt

# 3. Start the backend
uvicorn app.main:app --reload

# 4. In a new terminal, install & start the frontend
cd frontend
npm install
npm run dev

# 5. Open http://localhost:5173
```

## Optional: Groq API

Copy `backend/.env.example` to `backend/.env` and add your Groq API key for an additional LLM provider option.

```
GROQ_API_KEY=gsk_your_key_here
```

## Setup Script (Windows)

Double-click `setup.bat` to install all dependencies automatically.

## Project Structure

```
local-ai-engineer/
├── backend/
│   └── app/
│       ├── main.py              # FastAPI entry point
│       ├── config.py            # Configuration
│       ├── db/                  # SQLite database
│       ├── models/              # Pydantic schemas
│       ├── routers/             # API routes
│       └── services/
│           ├── llm/             # LLM providers (Ollama, Groq)
│           ├── rag/             # RAG engine (ChromaDB)
│           └── tools/           # AI tools
├── frontend/
│   └── src/
│       ├── api/                 # API client
│       ├── components/          # React components
│       └── App.jsx              # Main app
├── setup.bat
└── README.md
```

## Memory Requirements

- Ollama (7B model): ~4-6GB RAM
- all-MiniLM-L6-v2: ~200MB
- Python backend: ~200MB
- Node frontend: ~100MB
- **Total: ~5-7GB** (varies by model size)

For lower RAM usage, use a smaller model: `ollama pull qwen2.5:3b` or `ollama pull deepseek-coder:1.3b`.
