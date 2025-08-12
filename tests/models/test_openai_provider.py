import os
import sys
from unittest import mock

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import pytest

from core.models import ChatResponse
from core.providers.openai_provider import OpenAIProvider


class DummyStreamResponse:
    def __init__(self, lines):
        self._lines = lines

    def iter_lines(self):
        for l in self._lines:
            yield l


def test_openai_provider_non_streaming():
    with mock.patch("core.providers.openai_provider.requests.post") as mock_post:
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "hello"}}],
            "usage": {
                "prompt_tokens": 1,
                "completion_tokens": 2,
                "total_tokens": 3,
            },
        }
        mock_post.return_value = mock_response

        provider = OpenAIProvider(model="gpt-test", api_key="key")
        resp = provider.chat([{"role": "user", "content": "hi"}])

        assert isinstance(resp, ChatResponse)
        assert resp.message == "hello"
        assert resp.tokens_in == 1
        assert resp.tokens_out == 2
        assert resp.total_tokens == 3


def test_openai_provider_streaming():
    lines = [
        b'data: {"choices":[{"delta":{"content":"Hel"}}]}',
        b'data: {"choices":[{"delta":{"content":"lo"}}]}',
        b'data: {"choices":[{"delta":{}}],"usage":{"prompt_tokens":1,"completion_tokens":2,"total_tokens":3}}',
        b'data: [DONE]',
    ]
    mock_response = DummyStreamResponse(lines)
    with mock.patch("core.providers.openai_provider.requests.post", return_value=mock_response):
        provider = OpenAIProvider(model="gpt-test", api_key="key")
        gen = provider.chat([{"role": "user", "content": "hi"}], stream=True)

        chunks = []
        final = None
        for item in gen:
            if isinstance(item, ChatResponse):
                final = item
            else:
                chunks.append(item)

        assert chunks == ["Hel", "lo"]
        assert final is not None
        assert isinstance(final, ChatResponse)
        assert final.message == "Hello"
        assert final.tokens_in == 1
        assert final.tokens_out == 2
        assert final.total_tokens == 3

