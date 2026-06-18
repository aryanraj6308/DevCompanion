from functools import lru_cache
from app.config import EMBEDDING_MODEL


class Embedder:
    def __init__(self, model_name: str = None):
        self.model_name = model_name or EMBEDDING_MODEL
        self._model = None

    def _load(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name)

    def embed(self, text: str) -> list:
        self._load()
        return self._model.encode(text).tolist()

    def embed_batch(self, texts: list) -> list:
        self._load()
        return self._model.encode(texts).tolist()

    @property
    def dimension(self) -> int:
        self._load()
        return self._model.get_sentence_embedding_dimension()


@lru_cache()
def get_embedder() -> Embedder:
    return Embedder()
