from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Type


@dataclass
class ChatResponse:
    """Response information returned from a chat completion."""

    message: str
    tokens_in: int
    tokens_out: int
    total_tokens: int
    latency: float


class ModelRegistry:
    """Simple registry for provider classes."""

    _providers: Dict[str, Type[object]] = {}

    @classmethod
    def register(cls, name: str, provider: Type[object]) -> None:
        cls._providers[name] = provider

    @classmethod
    def get(cls, name: str) -> Type[object]:
        try:
            return cls._providers[name]
        except KeyError as exc:
            raise KeyError(f"Provider '{name}' is not registered") from exc


# Register built-in providers
from .providers.openai_provider import OpenAIProvider

ModelRegistry.register("openai", OpenAIProvider)

