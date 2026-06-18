from typing import List, Dict, Optional, Generator
from app.services.llm.base import LLMProvider
from app.services.llm.ollama import OllamaProvider
from app.services.llm.groq import GroqProvider
from app.config import DEFAULT_PROVIDER


class LLMRouter:
    def __init__(self):
        self.providers = {
            "ollama": OllamaProvider(),
            "groq": GroqProvider(),
        }
        self._default = DEFAULT_PROVIDER

    def get_provider(self, name: str = None) -> LLMProvider:
        name = name or self._default
        if name not in self.providers:
            name = "ollama"
        provider = self.providers[name]
        if name == "groq" and not provider.available:
            fallback = self.providers["ollama"]
            return fallback
        return provider

    def list_providers(self) -> List[dict]:
        result = []
        for name, provider in self.providers.items():
            result.append({
                "name": name,
                "available": getattr(provider, "available", True),
                "default_model": provider.default_model,
            })
        return result

    def generate(self, messages: List[Dict[str, str]], provider: str = None, **kwargs) -> str:
        prov = self.get_provider(provider)
        return prov.generate(messages, **kwargs)

    def generate_stream(self, messages: List[Dict[str, str]], provider: str = None, **kwargs) -> Generator[str, None, None]:
        prov = self.get_provider(provider)
        yield from prov.generate_stream(messages, **kwargs)


router = LLMRouter()
