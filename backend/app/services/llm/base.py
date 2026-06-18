from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Generator


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, messages: List[Dict[str, str]], stream: bool = False, **kwargs) -> str:
        ...

    @abstractmethod
    def generate_stream(self, messages: List[Dict[str, str]], **kwargs) -> Generator[str, None, None]:
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def default_model(self) -> str:
        ...
