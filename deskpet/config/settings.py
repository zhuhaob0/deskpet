"""Configuration management."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class PetConfig:
    type: str = "default"
    position_x: int = 100
    position_y: int = 100


@dataclass
class ChatConfig:
    handler: str = "static"
    responses_file: str | None = None


@dataclass
class AppConfig:
    pet: PetConfig = field(default_factory=PetConfig)
    chat: ChatConfig = field(default_factory=ChatConfig)
    run_on_startup: bool = False
    config_path: Path = Path.home() / ".deskpet" / "config.json"

    @classmethod
    def load(cls, path: Path | None = None) -> AppConfig:
        path = path or cls().config_path
        if path.exists():
            with open(path) as f:
                data = json.load(f)
            return cls.from_dict(data)
        return cls()

    def save(self, path: Path | None = None) -> None:
        path = path or self.config_path
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    def to_dict(self) -> dict[str, Any]:
        return {
            "pet": {"type": self.pet.type, "position_x": self.pet.position_x, "position_y": self.pet.position_y},
            "chat": {"handler": self.chat.handler, "responses_file": self.chat.responses_file},
            "run_on_startup": self.run_on_startup,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AppConfig:
        return cls(
            pet=PetConfig(**data.get("pet", {})),
            chat=ChatConfig(**data.get("chat", {})),
            run_on_startup=data.get("run_on_startup", False),
        )
