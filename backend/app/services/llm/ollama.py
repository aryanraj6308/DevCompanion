from typing import List, Dict, Generator
import httpx
from app.services.llm.base import LLMProvider
from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL


class OllamaProvider(LLMProvider):
    def __init__(self, base_url: str = None, model: str = None):
        self.base_url = (base_url or OLLAMA_BASE_URL).rstrip("/")
        self._model = model or OLLAMA_MODEL

    @property
    def name(self) -> str:
        return "ollama"

    @property
    def default_model(self) -> str:
        return self._model

    def generate(self, messages: List[Dict[str, str]], stream: bool = False, **kwargs) -> str:
        payload = {
            "model": kwargs.get("model", self._model),
            "messages": messages,
            "stream": False,
        }
        if "temperature" in kwargs:
            payload["temperature"] = kwargs["temperature"]
        if "max_tokens" in kwargs:
            payload["max_tokens"] = kwargs["max_tokens"]

        with httpx.Client(timeout=120.0) as client:
            resp = client.post(f"{self.base_url}/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data.get("message", {}).get("content", "")

    def generate_stream(self, messages: List[Dict[str, str]], **kwargs) -> Generator[str, None, None]:
        payload = {
            "model": kwargs.get("model", self._model),
            "messages": messages,
            "stream": True,
        }
        with httpx.Client(timeout=120.0) as client:
            with client.stream("POST", f"{self.base_url}/api/chat", json=payload) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if line:
                        import json
                        try:
                            data = json.loads(line)
                            content = data.get("message", {}).get("content", "")
                            if content:
                                yield content
                            if data.get("done", False):
                                break
                        except json.JSONDecodeError:
                            continue
