# DeskPet Agent Instructions

## Dependency Management
- Use Tsinghua mirror: `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple`

## Commands
```bash
pip install -e ".[dev]"    # Install with dev dependencies
deskpet                    # Run (Windows) or python -m deskpet.main (Linux)
ruff check .               # Linter
python scripts/generate_sprites.py  # Generate test sprites
```

## Architecture
- **deskpet/main.py**: Entry point. `DeskPetApp` class runs ~30fps update loop in daemon thread.
- **pet/engine.py**: `PetEngine` manages behavior state machine. Must call `start()` before `tick()`.
- **commands/**: `/<cmd>` registry. Inherit `Command`, register via `get_command_registry()`.
- **chat/**: Natural language handlers. Implement `ChatHandler`, register via `get_registry()`.
- **ui/chat_dialog.py**: PyQt6 dialog. Call `set_dependencies()` before `show()`.

## Key Patterns
- **PetEngine initialization**: `PetEngine(pet_type, resource_dir / "pets", bounds=ScreenBounds(...))` then `engine.start()`
- **ScreenBounds**: `ScreenBounds(width, height, margin=64)` limits pet movement area
- **Two registries**: Command (`/walk`) and chat (natural language) systems are separate
- **Overlay**: PyQt6 transparent window on Windows, `ConsoleOverlay` on Linux

## Config
- Auto-saves to `~/.deskpet/config.json`
- Logs to `log/deskpet.log` (cleared on each run)
- Fields: `pet.type`, `pet.position_x/y`, `chat.handler`, `chat.responses_file`

## Build
```bash
pyinstaller deskpet.spec --clean
# Output: dist/DeskPet/
```

## Verification
- Run `ruff check .` (no tests directory yet)