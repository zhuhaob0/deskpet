# DeskPet Agent Instructions

## Project Overview

Desktop pet application for Windows with transparent overlay window, system tray integration, and extensible command/chat systems.

## Key Commands

```bash
pip install -e ".[dev]"  # Install with dev dependencies
deskpet  # or: python -m deskpet.main
python scripts/generate_sprites.py  # Generate test sprites
```

## Architecture

- **pet/engine.py**: PetEngine class manages behavior state machine. Call `tick()` at ~30fps to get sprite/position updates.
- **commands/**: Command registry for `/<cmd>` syntax. Inherit `Command` base class to add custom commands.
- **chat/**: Natural language responses via ChatHandler protocol. Register handlers to `get_registry()`.
- **ui/chat_dialog.py**: PyQt6 dialog, call `set_dependencies()` before showing.

## Important Notes

- PetEngine requires `start()` before `tick()`. Pass `ScreenBounds` to limit movement area.
- Command system and chat system are separate: commands are for structured control (`/walk`), chat is for natural language.
- Overlay uses PyQt6 transparent window. Windows only for now.
- Config auto-saves to `%USERPROFILE%\.deskpet\config.json`.
