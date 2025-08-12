from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Generator, Any

from ..models import ChatResponse


class Provider(ABC):
    @abstractmethod
    def chat(
        self, messages: Iterable[dict], stream: bool = False, **kwargs: Any
    ) -> Any:
        """Send chat messages to the model.

        When ``stream`` is ``False`` a :class:`ChatResponse` should be returned.
        When ``stream`` is ``True`` an iterator yielding chunks of the
        response should be returned. The final iterator item should be a
        :class:`ChatResponse` containing the accumulated message and usage
        statistics.
        """

