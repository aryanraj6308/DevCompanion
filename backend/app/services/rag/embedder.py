from functools import lru_cache
from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2


class Embedder:
    def __init__(self):
        self._model = ONNXMiniLM_L6_V2(preferred_providers=["CPUExecutionProvider"])

    def embed(self, text: str) -> list:
        return self._model([text])[0]

    def embed_batch(self, texts: list) -> list:
        return self._model(texts)

    @property
    def dimension(self) -> int:
        return 384


@lru_cache()
def get_embedder() -> Embedder:
    return Embedder()
