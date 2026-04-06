"""Console overlay for non-Windows platforms (development/testing)."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable

from deskpet.pet.overlay import PetOverlay


logger = logging.getLogger(__name__)


class ConsoleOverlay(PetOverlay):
    def __init__(self, on_double_click: Callable[[], None] | None = None):
        super().__init__(on_double_click)
        self._last_sprite = ""
        self._last_position = (0, 0)

    def show(self, sprite_path: str, position: tuple[int, int]) -> None:
        self._window = True
        self._last_sprite = sprite_path
        self._last_position = position
        logger.info(f"Overlay show: sprite={Path(sprite_path).name}, pos={position}")

    def move(self, position: tuple[int, int]) -> None:
        if position != self._last_position:
            self._last_position = position

    def update_sprite(self, sprite_path: str) -> None:
        if sprite_path != self._last_sprite:
            self._last_sprite = sprite_path
            logger.debug(f"Sprite update: {Path(sprite_path).name}")

    def hide(self) -> None:
        self._window = None
        logger.info("Overlay hidden")
