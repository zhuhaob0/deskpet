"""Built-in commands for pet interactions."""

from __future__ import annotations

from deskpet.commands.base import Command, CommandContext, CommandResult, CommandRegistry
from deskpet.pet.engine import Behavior, PetEngine


class WalkCommand(Command):
    name = "walk"
    aliases = ["go", "move"]
    description = "Make pet walk to a position or randomly"
    usage = "/walk [x y] or /walk random"

    def execute(self, args: list[str], pet_engine: PetEngine | None = None) -> CommandResult:
        if pet_engine is None:
            return CommandResult(False, "Pet engine not available")

        if not args:
            pet_engine.command(Behavior.WALK, 0.0)
            return CommandResult(True, "Walking to a random position...")

        if args[0].lower() == "random":
            pet_engine.command(Behavior.WALK, 0.0)
            return CommandResult(True, "Walking to a random position...")

        if len(args) >= 2:
            try:
                x, y = int(args[0]), int(args[1])
                pet_engine.walk_to(x, y)
                return CommandResult(True, f"Walking to ({x}, {y})...")
            except ValueError:
                return CommandResult(False, "Invalid coordinates. Usage: /walk x y")

        return CommandResult(False, f"Usage: {self.usage}")


class SleepCommand(Command):
    name = "sleep"
    aliases = ["nap", "rest"]
    description = "Make pet sleep for a duration"
    usage = "/sleep [seconds]"

    def execute(self, args: list[str], pet_engine: PetEngine | None = None) -> CommandResult:
        if pet_engine is None:
            return CommandResult(False, "Pet engine not available")

        duration = 8.0
        if args:
            try:
                duration = float(args[0])
            except ValueError:
                return CommandResult(False, "Invalid duration. Usage: /sleep [seconds]")

        pet_engine.command(Behavior.SLEEP, duration)
        return CommandResult(True, f"Zzz... sleeping for {duration} seconds")


class EatCommand(Command):
    name = "eat"
    aliases = ["feed", "nom"]
    description = "Make pet eat"
    usage = "/eat"

    def execute(self, args: list[str], pet_engine: PetEngine | None = None) -> CommandResult:
        if pet_engine is None:
            return CommandResult(False, "Pet engine not available")

        duration = 3.0
        if args:
            try:
                duration = float(args[0])
            except ValueError:
                pass

        pet_engine.command(Behavior.EAT, duration)
        return CommandResult(True, "Nom nom nom...")


class PlayCommand(Command):
    name = "play"
    aliases = ["fun", "game"]
    description = "Make pet play"
    usage = "/play"

    def execute(self, args: list[str], pet_engine: PetEngine | None = None) -> CommandResult:
        if pet_engine is None:
            return CommandResult(False, "Pet engine not available")

        duration = 6.0
        if args:
            try:
                duration = float(args[0])
            except ValueError:
                pass

        pet_engine.command(Behavior.PLAY, duration)
        return CommandResult(True, "Wheee! Having fun!")


class HelpCommand(Command):
    name = "help"
    aliases = ["?"]
    description = "Show help for commands"
    usage = "/help [command]"

    def execute(self, args: list[str], pet_engine: PetEngine | None = None) -> CommandResult:
        registry = get_command_registry()

        if not args:
            commands = registry.list_commands()
            lines = ["Available commands:", ""]
            for cmd in commands:
                lines.append(f"  /{cmd.name:<10} {cmd.description}")
            lines.append("")
            lines.append("Type /help <command> for details")
            return CommandResult(True, "\n".join(lines))

        cmd_name = args[0].lstrip("/")
        command = registry.get(cmd_name)
        if not command:
            return CommandResult(False, f"Unknown command: {cmd_name}")

        msg = f"/{command.name} - {command.description}\nUsage: {command.usage}"
        if command.aliases:
            msg += f"\nAliases: {', '.join('/' + a for a in command.aliases)}"
        return CommandResult(True, msg)


class StatusCommand(Command):
    name = "status"
    aliases = ["info", "state"]
    description = "Show current pet status"
    usage = "/status"

    def execute(self, args: list[str], pet_engine: PetEngine | None = None) -> CommandResult:
        if pet_engine is None:
            return CommandResult(False, "Pet engine not available")

        state = pet_engine.get_state()
        lines = [
            f"Name: {state.name}",
            f"Behavior: {state.behavior.name}",
            f"Position: ({state.position_x}, {state.position_y})",
        ]
        return CommandResult(True, "\n".join(lines))


class ConfigCommand(Command):
    name = "config"
    aliases = ["set"]
    description = "Configure pet settings"
    usage = "/config <setting> <value>"

    def execute(self, args: list[str], pet_engine: PetEngine | None = None) -> CommandResult:
        if len(args) < 2:
            return CommandResult(False, f"Usage: {self.usage}")

        setting = args[0].lower()
        value = args[1]

        config_commands = {
            "speed": ("walk_speed", float),
            "name": ("name", str),
        }

        if setting in config_commands:
            attr, type_fn = config_commands[setting]
            return CommandResult(
                True, f"Config '{setting}' set to '{value}' (config not persisted yet)"
            )

        return CommandResult(False, f"Unknown setting: {setting}")


def get_command_registry():
    from deskpet.commands.base import _default_registry

    if _default_registry is None:
        from deskpet.commands.base import CommandRegistry

        _default_registry = CommandRegistry()
        _register_builtin_commands(_default_registry)
    return _default_registry
