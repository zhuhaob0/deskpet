"""Pet sprite management."""

from __future__ import annotations

from pathlib import Path
from typing import Generator

from deskpet.pet.engine import Behavior


class SpriteManager:
    def __init__(self, sprite_dir: Path):
        self.sprite_dir = sprite_dir

    def get_sprite(self, behavior: Behavior, frame: int = 0) -> str:
        behavior_name = behavior.name.lower()
        sprite_path = self.sprite_dir / f"{behavior_name}_{frame:02d}.png"
        if sprite_path.exists():
            return str(sprite_path)
        return str(self.sprite_dir / "idle_00.png")

    def list_available(self) -> list[str]:
        if not self.sprite_dir.exists():
            return []
        return [f.stem for f in self.sprite_dir.glob("*.png")]
