"""Pet sprite management."""

from __future__ import annotations

from pathlib import Path

from deskpet.pet.engine import Behavior


class SpriteManager:
    def __init__(self, sprite_dir: Path):
        self.sprite_dir = sprite_dir

    def get_sprite(self, behavior: Behavior, frame: int = 0) -> str:
        behavior_name = behavior.name.lower()
        sprite_path = self.sprite_dir / behavior_name / f"{behavior_name}_{frame:02d}.png"
        if sprite_path.exists():
            return str(sprite_path)
        sprite_path = self.sprite_dir / behavior_name / "idle_00.png"
        if sprite_path.exists():
            return str(sprite_path)
        return str(self.sprite_dir / "idle" / "idle_00.png")

    def list_behaviors(self) -> list[str]:
        if not self.sprite_dir.exists():
            return []
        behaviors = []
        for item in sorted(self.sprite_dir.iterdir()):
            if item.is_dir() and (item / f"{item.name}_00.png").exists():
                behaviors.append(item.name)
        return behaviors

    def get_frame_count(self, behavior: str) -> int:
        behavior_dir = self.sprite_dir / behavior
        if not behavior_dir.exists():
            return 1
        count = 0
        for f in behavior_dir.glob(f"{behavior}_*.png"):
            count += 1
        return max(count, 1)

    def behavior_exists(self, behavior: str) -> bool:
        return (self.sprite_dir / behavior / f"{behavior}_00.png").exists()
