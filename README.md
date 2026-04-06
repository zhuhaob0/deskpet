# DeskPet

A customizable desktop pet application for Windows. Run applications on your desktop with an adorable pet companion that can walk, sleep, eat, and chat with you.

## Features

- **System Tray Integration** - Runs minimized in the Windows taskbar
- **Multiple Pet Types** - Switch between different pet types via tray menu
- **Interactive Behaviors** - Command your pet to walk, sleep, eat, or play
- **Double-Click Chat** - Open chat dialog to interact with your pet
- **Extensible Chat System** - Plugin architecture for AI integration

## Requirements

- Python 3.10+
- Windows OS (for full functionality)
- PyQt6 (for transparent overlay window)
- pystray (for system tray, Windows/Linux)
- Pillow (for image handling)

## Installation

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -e ".[dev]"
```

## Usage

### Windows

```bash
deskpet
```

### Linux (Console Mode)

On Linux without GTK/pystray, the app runs in console mode:

```bash
python -m deskpet.main
```

Available commands:
- `walk` - Random walk
- `sleep` - Sleep for 8s
- `eat` - Eat for 3s
- `play` - Play for 6s
- `status` - Show pet status
- `quit` - Exit

## Project Structure

```
deskpet/
├── deskpet/
│   ├── main.py           # App entry point & lifecycle
│   ├── tray.py           # System tray management
│   ├── pet/              # Pet engine & rendering
│   │   ├── engine.py     # State machine & behaviors
│   │   ├── sprites.py    # Sprite management
│   │   ├── overlay.py    # Transparent window overlay
│   │   └── overlay_win.py # Windows implementation
│   ├── chat/             # Chat system (for natural language)
│   │   ├── base.py       # ChatHandler protocol
│   │   ├── static.py     # Fixed response handler
│   │   └── registry.py   # Handler registry
│   ├── commands/         # Command system (for /cmd syntax)
│   │   └── __init__.py   # Built-in commands
│   ├── ui/               # UI components
│   │   └── chat_dialog.py # Chat dialog window
│   └── config/           # Configuration
│       └── settings.py   # AppConfig dataclass
├── scripts/              # Utility scripts
│   └── generate_sprites.py
└── resources/
    └── pets/             # Pet sprite images
```

## Pet Behaviors

| Behavior | Duration | Description |
|----------|----------|-------------|
| IDLE | - | Default state, pet occasionally walks randomly |
| WALK | 5s | Moves toward target position |
| SLEEP | 8s | Sleep animation |
| EAT | 3s | Eating animation |
| PLAY | 6s | Playing animation |

### Behavior API

```python
from deskpet.pet import PetEngine, Behavior

engine = PetEngine("cat", resource_dir / "pets")

# Command behaviors
engine.command(Behavior.SLEEP, duration=5.0)
engine.command(Behavior.EAT, duration=3.0)

# Walk to specific position
engine.walk_to(500, 300)

# Walk to random position
engine.walk_random()

# Set behavior change callback
engine.set_behavior_callback(lambda b: print(f"Now: {b.name}"))
```

## Chat Dialog Commands

Double-click the pet to open the chat dialog. Use `/<command>` syntax to control your pet:

| Command | Aliases | Description |
|---------|---------|-------------|
| `/walk [x y]` | `go`, `move` | Walk to coordinates or randomly |
| `/sleep [sec]` | `nap`, `rest` | Take a nap (default 8s) |
| `/eat [sec]` | `feed`, `nom` | Have a snack (default 3s) |
| `/play [sec]` | `fun`, `game` | Play around (default 6s) |
| `/status` | `info`, `state` | Show current status |
| `/config <key> <val>` | `set` | Configure settings |
| `/help [cmd]` | `?` | Show help |

### Adding Custom Commands

```python
from deskpet.commands.base import Command, CommandResult, get_command_registry

class CustomCommand(Command):
    name = "mycmd"
    aliases = ["mc"]
    description = "My custom command"
    usage = "/mycmd <arg>"

    def execute(self, args: list[str], pet_engine=None) -> CommandResult:
        if not args:
            return CommandResult(False, f"Usage: {self.usage}")
        return CommandResult(True, f"Executed with: {args[0]}")

# Register the command
get_command_registry().register(CustomCommand())
```

## Adding Pet Sprites

Place sprite images in `resources/pets/<pet_type>/` with naming convention:

```
<behavior>_<frame>.png
```

Example: `idle_00.png`, `walk_01.png`, `sleep_02.png`

Supported behaviors: `idle`, `walk`, `sleep`, `eat`, `play`

Generate placeholder sprites for testing:

```bash
python scripts/generate_sprites.py
```

## Extending Chat System

Implement the `ChatHandler` protocol to add custom chat backends for natural language responses:

```python
from deskpet.chat.base import ChatHandler
from deskpet.chat.registry import get_registry

class AIDemoHandler:
    def handle(self, message: str, context: dict) -> str:
        # Your AI integration here
        return "AI response"

    def is_available(self) -> bool:
        return True

get_registry().register(AIDemoHandler())
```

**Note:** Chat handlers are for natural language responses. For structured commands, use the [command system](#adding-custom-commands) instead.

## Configuration

Config is stored at `%USERPROFILE%\.deskpet\config.json`:

```json
{
  "pet": {
    "type": "cat",
    "position_x": 100,
    "position_y": 100
  },
  "chat": {
    "handler": "static",
    "responses_file": null
  },
  "run_on_startup": false
}
```

## Development

```bash
pip install -e ".[dev]"
ruff check .
pytest
```

## License

MIT
