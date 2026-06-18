from fastapi import APIRouter, HTTPException

from app.models.document import IndexRequest, IndexResponse, QueryRequest, QueryResponse, QueryResult
from app.services.rag.engine import get_rag_engine

router = APIRouter(prefix="/api/rag", tags=["rag"])


@router.post("/index", response_model=IndexResponse)
def index_document(req: IndexRequest):
    engine = get_rag_engine()
    try:
        chunk_count = engine.index(req.content, req.filename, req.doc_metadata)
        return IndexResponse(chunk_count=chunk_count, filename=req.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query", response_model=QueryResponse)
def query_documents(req: QueryRequest):
    engine = get_rag_engine()
    try:
        results = engine.query(req.query, req.n_results)
        return QueryResponse(
            query=req.query,
            results=[QueryResult(**r) for r in results],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
def get_stats():
    engine = get_rag_engine()
    return {
        "total_chunks": engine.count_documents(),
        "collection": engine.collection_name,
    }
