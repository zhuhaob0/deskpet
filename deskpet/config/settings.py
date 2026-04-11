"""Configuration management."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


def _get_default_config_path() -> Path:
    if getattr(__import__("sys"), "frozen", False):
        base = Path(__import__("sys")._MEIPASS).parent
    else:
        base = Path(__file__).parent.parent.parent
    return base / ".deskpet" / "config.json"


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
    config_path: Path = field(default_factory=_get_default_config_path)

    @classmethod
    def load(cls, path: Path | None = None) -> AppConfig:
        if path is None:
            path = _get_default_config_path()
        if path.exists():
            with open(path) as f:
                data = json.load(f)
            return cls.from_dict(data)
        return cls()

    def save(self, path: Path | None = None) -> None:
        if path is None:
            path = self.config_path
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    def to_dict(self) -> dict[str, Any]:
        return {
            "pet": {
                "type": self.pet.type,
                "position_x": self.pet.position_x,
                "position_y": self.pet.position_y,
            },
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
