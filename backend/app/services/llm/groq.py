from typing import List, Dict, Generator
import httpx
import json
from app.services.llm.base import LLMProvider
from app.config import GROQ_API_KEY, GROQ_MODEL


class GroqProvider(LLMProvider):
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or GROQ_API_KEY
        self._model = model or GROQ_MODEL
        self.base_url = "https://api.groq.com/openai/v1"

    @property
    def name(self) -> str:
        return "groq"

    @property
    def default_model(self) -> str:
        return self._model

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def generate(self, messages: List[Dict[str, str]], stream: bool = False, **kwargs) -> str:
        if not self.available:
            raise RuntimeError("Groq API key not configured")

        payload = {
            "model": kwargs.get("model", self._model),
            "messages": messages,
            "stream": False,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        with httpx.Client(timeout=120.0) as client:
            resp = client.post(f"{self.base_url}/chat/completions", json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "")

    def generate_stream(self, messages: List[Dict[str, str]], **kwargs) -> Generator[str, None, None]:
        if not self.available:
            raise RuntimeError("Groq API key not configured")

        payload = {
            "model": kwargs.get("model", self._model),
            "messages": messages,
            "stream": True,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        with httpx.Client(timeout=120.0) as client:
            with client.stream("POST", f"{self.base_url}/chat/completions", json=payload, headers=headers) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]
                        if data_str.strip() == "[DONE]":
                            break
                        try:
                            data = json.loads(data_str)
                            delta = data.get("choices", [{}])[0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                yield content
                        except json.JSONDecodeError:
                            continue
