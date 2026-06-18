import chromadb
from chromadb.config import Settings
from app.config import CHROMA_DIR


class ChromaManager:
    def __init__(self, persist_dir: str = None):
        self.persist_dir = persist_dir or CHROMA_DIR
        self.client = chromadb.PersistentClient(
            path=self.persist_dir,
            settings=Settings(anonymized_telemetry=False),
        )

    def get_or_create_collection(self, name: str = "project_knowledge"):
        return self.client.get_or_create_collection(name=name)

    def delete_collection(self, name: str):
        try:
            self.client.delete_collection(name)
        except ValueError:
            pass

    def list_collections(self):
        return self.client.list_collections()


_manager = None


def get_chroma() -> ChromaManager:
    global _manager
    if _manager is None:
        _manager = ChromaManager()
    return _manager
