"""Transparent overlay window for displaying pet."""

from __future__ import annotations

from typing import Callable


class PetOverlay:
    def __init__(
        self,
        on_double_click: Callable[[], None] | None = None,
        on_position_changed: Callable[[int, int], None] | None = None,
    ):
        self.on_double_click = on_double_click
        self._on_position_changed = on_position_changed
        self._window = None

    def show(self, sprite_path: str, position: tuple[int, int]) -> None:
        raise NotImplementedError("Subclass must implement show()")

    def move(self, position: tuple[int, int]) -> None:
        raise NotImplementedError("Subclass must implement move()")

    def update_sprite(self, sprite_path: str) -> None:
        raise NotImplementedError("Subclass must implement update_sprite()")

    def hide(self) -> None:
        if self._window:
            self._window.close()
            self._window = None

    @staticmethod
    def create(platform: str = "windows") -> PetOverlay:
        if platform == "windows":
            from deskpet.pet.overlay_win import WindowsOverlay

            return WindowsOverlay()
        raise NotImplementedError(f"Platform {platform} not supported")
