# DeskPet Agent Instructions

## Key Commands

```bash
pip install -e ".[dev]"    # Install with dev dependencies
deskpet                    # Run app (Windows) or python -m deskpet.main (Linux)
ruff check .               # Linter
python scripts/generate_sprites.py  # Generate test sprites
```

## Architecture

- **deskpet/main.py**: App entry point, runs update loop at ~30fps
- **pet/engine.py**: PetEngine manages behavior state machine. Must call `start()` before `tick()`.
- **commands/**: Registry for `/<cmd>` syntax. Inherit `Command` base class.
- **chat/**: Natural language handlers via ChatHandler protocol. Register to `get_registry()`.
- **ui/chat_dialog.py**: PyQt6 dialog - call `set_dependencies()` before `show()`.

## Important Notes

- PetEngine requires `start()` before `tick()`. Pass `ScreenBounds` to limit movement area.
- Command system (`/walk`) and chat system (natural language) are separate registries.
- Overlay: PyQt6 transparent window on Windows, console mode on Linux.
- Config auto-saves to `%USERPROFILE%\.deskpet\config.json`.
- No tests directory yet - run `ruff check .` for verification.

## Directory Ownership

- `pet/`: Behavior state machine, sprite management, overlay rendering
- `chat/`: Natural language response handlers
- `commands/`: Slash commands (/walk, /sleep, etc.)
- `ui/`: PyQt6 dialogs
- `config/`: AppConfig dataclass