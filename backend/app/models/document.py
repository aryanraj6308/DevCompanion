from pydantic import BaseModel
from typing import List, Optional


class IndexRequest(BaseModel):
    content: str
    filename: str
    doc_metadata: Optional[dict] = None


class IndexResponse(BaseModel):
    chunk_count: int
    filename: str


class QueryRequest(BaseModel):
    query: str
    n_results: int = 5


class QueryResult(BaseModel):
    content: str
    filename: str
    score: float


class QueryResponse(BaseModel):
    query: str
    results: List[QueryResult]
