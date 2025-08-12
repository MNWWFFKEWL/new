from __future__ import annotations

import json
import os
import time
from typing import Iterable, Iterator, Any

import requests

from .base import Provider
from ..models import ChatResponse


class OpenAIProvider(Provider):
    """Provider implementation using OpenAI's Chat Completions API."""

    api_url = "https://api.openai.com/v1/chat/completions"

    def __init__(self, model: str, api_key: str | None = None) -> None:
        self.model = model
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")

    def chat(
        self, messages: Iterable[dict], stream: bool = False, **_: Any
    ) -> Any:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"model": self.model, "messages": list(messages), "stream": stream}
        start = time.time()
        response = requests.post(
            self.api_url, headers=headers, json=payload, stream=stream
        )
        if stream:
            return self._streaming_response(response, start)
        data = response.json()
        usage = data.get("usage", {})
        latency = time.time() - start
        message = data["choices"][0]["message"]["content"]
        return ChatResponse(
            message=message,
            tokens_in=usage.get("prompt_tokens", 0),
            tokens_out=usage.get("completion_tokens", 0),
            total_tokens=usage.get("total_tokens", 0),
            latency=latency,
        )

    def _streaming_response(self, response: requests.Response, start: float) -> Iterator[Any]:
        """Yield chunks of the streaming response and final ChatResponse."""
        final_message = ""
        tokens_in = tokens_out = total_tokens = 0
        for line in response.iter_lines():
            if not line:
                continue
            if line.startswith(b"data: "):
                line = line[len(b"data: ") :]
            if line == b"[DONE]":
                break
            data = json.loads(line)
            delta = data["choices"][0].get("delta", {}).get("content")
            if delta:
                final_message += delta
                yield delta
            usage = data.get("usage")
            if usage:
                tokens_in = usage.get("prompt_tokens", 0)
                tokens_out = usage.get("completion_tokens", 0)
                total_tokens = usage.get("total_tokens", 0)
        latency = time.time() - start
        yield ChatResponse(
            message=final_message,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            total_tokens=total_tokens,
            latency=latency,
        )

