"""Base chat handler interface - implement this for custom chat backends."""

from abc import ABC, abstractmethod
from typing import Protocol


class ChatHandler(Protocol):
    """Protocol for chat handlers."""

    @abstractmethod
    def handle(self, message: str, context: dict) -> str:
        """Process user message and return response."""
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Check if handler is ready to process messages."""
        ...
