import hashlib
from typing import List, Optional
from app.services.rag.chroma_client import get_chroma
from app.config import CHUNK_SIZE, CHUNK_OVERLAP


class RAGEngine:
    def __init__(self, collection_name: str = "project_knowledge"):
        self.collection_name = collection_name
        self.chroma = get_chroma()
        self.collection = self.chroma.get_or_create_collection(collection_name)

    def _chunk_text(self, text: str) -> List[str]:
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + CHUNK_SIZE, len(text))
            chunks.append(text[start:end])
            start += CHUNK_SIZE - CHUNK_OVERLAP
        return chunks

    def index(self, content: str, filename: str, metadata: Optional[dict] = None) -> int:
        chunks = self._chunk_text(content)
        if not chunks:
            return 0

        ids = []
        metadatas = []
        documents = []

        for i, chunk in enumerate(chunks):
            chunk_id = hashlib.md5(f"{filename}:{i}:{chunk[:50]}".encode()).hexdigest()
            ids.append(chunk_id)
            documents.append(chunk)
            metadatas.append({
                "filename": filename,
                "chunk_index": i,
                "total_chunks": len(chunks),
                **(metadata or {}),
            })

        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
        )
        return len(chunks)

    def query(self, query_text: str, n_results: int = 5) -> List[dict]:
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
        )

        output = []
        if results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                output.append({
                    "content": doc,
                    "filename": results["metadatas"][0][i].get("filename", "unknown"),
                    "score": float(results["distances"][0][i]) if results.get("distances") else 0.0,
                })
        return output

    def count_documents(self) -> int:
        return self.collection.count()

    def get_context(self, query_text: str, n_results: int = 3) -> str:
        results = self.query(query_text, n_results)
        if not results:
            return ""
        context_parts = []
        for r in results:
            context_parts.append(f"[From {r['filename']}]:\n{r['content']}")
        return "\n\n".join(context_parts)


_engine = None


def get_rag_engine() -> RAGEngine:
    global _engine
    if _engine is None:
        _engine = RAGEngine()
    return _engine
