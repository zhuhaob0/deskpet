"""Chat module - extensible chat handlers."""

from deskpet.chat.base import ChatHandler
from deskpet.chat.registry import ChatRegistry, get_registry
from deskpet.chat.static import StaticChatHandler, StaticChatHandlerWithVariants

__all__ = [
    "ChatHandler",
    "ChatRegistry",
    "StaticChatHandler",
    "StaticChatHandlerWithVariants",
    "get_registry",
]
