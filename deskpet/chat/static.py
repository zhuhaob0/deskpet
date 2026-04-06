"""Fixed/static response chat handler."""

from __future__ import annotations

from typing import Any

from deskpet.chat.base import ChatHandler


class StaticChatHandler(ChatHandler):
    def __init__(self, responses: dict[str, str] | None = None):
        self._responses = responses or {}
        self._default = "I'm not sure how to respond to that."

    def add_response(self, keyword: str, response: str) -> None:
        self._responses[keyword.lower()] = response

    def handle(self, message: str, context: dict[str, Any]) -> str:
        msg_lower = message.lower().strip()
        for keyword, response in self._responses.items():
            if keyword in msg_lower:
                return response
        return self._default

    def is_available(self) -> bool:
        return True


class StaticChatHandlerWithVariants(StaticChatHandler):
    def __init__(self, responses: dict[str, list[str]] | None = None):
        super().__init__()
        self._responses = {}
        self._variants: dict[str, list[str]] = responses or {}

    def add_response(self, keyword: str, responses: str | list[str]) -> None:
        if isinstance(responses, list):
            self._variants[keyword.lower()] = responses
        else:
            super().add_response(keyword, responses)

    def handle(self, message: str, context: dict[str, Any]) -> str:
        msg_lower = message.lower().strip()
        for keyword, variants in self._variants.items():
            if keyword in msg_lower:
                import random
                return random.choice(variants)
        return super().handle(message, context)
