"""Command system for pet interactions."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from deskpet.pet.engine import PetEngine


@dataclass
class CommandResult:
    success: bool
    message: str
    data: dict[str, Any] | None = None


class Command(ABC):
    name: str = ""
    aliases: list[str] = []
    description: str = ""
    usage: str = ""
    permission: str = "user"

    @abstractmethod
    def execute(self, args: list[str], pet_engine: "PetEngine | None" = None) -> CommandResult:
        """Execute the command with given arguments."""
        ...

    def get_full_name(self) -> str:
        return self.name

    def matches(self, name: str) -> bool:
        name = name.lower().lstrip("/")
        return name == self.name.lower() or name in [a.lower() for a in self.aliases]


@dataclass
class CommandContext:
    pet_engine: "PetEngine | None"
    user_data: dict[str, Any]


class CommandRegistry:
    def __init__(self):
        self._commands: dict[str, Command] = {}
        self._aliases: dict[str, str] = {}

    def register(self, command: Command) -> None:
        self._commands[command.name.lower()] = command
        for alias in command.aliases:
            self._aliases[alias.lower()] = command.name.lower()

    def unregister(self, name: str) -> None:
        name = name.lower()
        if name in self._commands:
            cmd = self._commands.pop(name)
            for alias in cmd.aliases:
                self._aliases.pop(alias.lower(), None)

    def get(self, name: str) -> Command | None:
        name = name.lower().lstrip("/")
        if name in self._commands:
            return self._commands[name]
        if name in self._aliases:
            return self._commands[self._aliases[name]]
        return None

    def list_commands(self, permission: str = "user") -> list[Command]:
        return [cmd for cmd in self._commands.values() if cmd.permission == permission]

    def execute(
        self,
        input_str: str,
        context: CommandContext,
    ) -> CommandResult:
        parts = input_str.strip().split(maxsplit=1)
        if not parts:
            return CommandResult(False, "No command provided")

        cmd_name = parts[0]
        args: list[str] = []
        if len(parts) > 1:
            args = parts[1].split()

        command = self.get(cmd_name)
        if not command:
            return CommandResult(False, f"Unknown command: {cmd_name}")

        try:
            return command.execute(args, context.pet_engine)
        except Exception as e:
            return CommandResult(False, f"Command error: {e}")


_default_registry: CommandRegistry | None = None


def get_command_registry() -> CommandRegistry:
    global _default_registry
    if _default_registry is None:
        _default_registry = CommandRegistry()
        _register_builtin_commands(_default_registry)
    return _default_registry


def _register_builtin_commands(registry: CommandRegistry) -> None:
    from deskpet.commands import (
        WalkCommand,
        SleepCommand,
        EatCommand,
        PlayCommand,
        HelpCommand,
        StatusCommand,
        ConfigCommand,
    )

    registry.register(WalkCommand())
    registry.register(SleepCommand())
    registry.register(EatCommand())
    registry.register(PlayCommand())
    registry.register(HelpCommand())
    registry.register(StatusCommand())
    registry.register(ConfigCommand())
