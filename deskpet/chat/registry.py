"""Chat handler registry for extensible chat backends."""

from __future__ import annotations

from typing import Any

from deskpet.chat.base import ChatHandler


class ChatRegistry:
    def __init__(self):
        self._handlers: list[ChatHandler] = []

    def register(self, handler: ChatHandler) -> None:
        self._handlers.append(handler)

    def unregister(self, handler: ChatHandler) -> None:
        if handler in self._handlers:
            self._handlers.remove(handler)

    def send(self, message: str, context: dict[str, Any] | None = None) -> str | None:
        context = context or {}
        for handler in self._handlers:
            if handler.is_available():
                return handler.handle(message, context)
        return None


_default_registry: ChatRegistry | None = None


def get_registry() -> ChatRegistry:
    global _default_registry
    if _default_registry is None:
        _default_registry = ChatRegistry()
    return _default_registry
