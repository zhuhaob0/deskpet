# DeskPet

A customizable desktop pet application for Windows. Run a cute pet on your desktop that can walk, sleep, eat, play, and chat with you.

## Features

- **Transparent Overlay** - Pet displays on desktop with transparent background
- **System Tray Integration** - Runs minimized in the Windows taskbar
- **Multiple Pet Types** - Switch between cat, dog, and default pets via tray menu
- **Interactive Behaviors** - Command your pet via chat dialog or tray menu
- **Drag & Drop** - Drag the pet to move it anywhere on screen
- **Double-Click Chat** - Open chat dialog to interact with your pet
- **Extensible Architecture** - Plugin architecture for commands and AI chat integration

## Requirements

- Python 3.10+
- Windows OS
- PyQt6 (for transparent overlay and system tray)

## Installation

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -e ".[dev]"
```

## Usage

### Windows

```bash
python -m deskpet.main
```

### Linux (Console Mode)

```bash
python -m deskpet.main
```

Available console commands:
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
│   ├── tray.py           # System tray management (PyQt6)
│   ├── pet/              # Pet engine & rendering
│   │   ├── engine.py     # State machine & behaviors
│   │   ├── sprites.py    # Sprite management
│   │   ├── overlay.py    # Abstract overlay base
│   │   └── overlay_win.py # Windows transparent window
│   ├── chat/             # Natural language chat system
│   │   ├── base.py       # ChatHandler protocol
│   │   ├── static.py     # Fixed response handler
│   │   └── registry.py   # Handler registry
│   ├── commands/         # Slash command system (/cmd)
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

| Behavior | Default Duration | Description |
|----------|-----------------|-------------|
| IDLE | - | Default state, occasionally walks randomly |
| WALK | 5s | Moves toward target position (or random if no target) |
| SLEEP | 8s | Sleep animation |
| EAT | 3s | Eating animation |
| PLAY | 6s | Playing animation |

### Behavior API

```python
from deskpet.pet.engine import PetEngine, Behavior

engine = PetEngine("cat", resource_dir / "pets")

# Command behaviors (timed)
engine.command(Behavior.SLEEP, duration=5.0)
engine.command(Behavior.EAT, duration=3.0)

# Walk to specific position
engine.walk_to(500, 300)

# Walk to random position
engine.command(Behavior.WALK, duration=0)  # 0 = continuous random walking

# Set behavior change callback
engine.set_behavior_callback(lambda b: print(f"Now: {b.name}"))
```

## Chat Dialog Commands

Double-click the pet to open the chat dialog. Use `/<command>` syntax:

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

get_command_registry().register(CustomCommand())
```

## Pet Sprites

### Directory Structure

```
resources/pets/
├── icon.png              # App tray icon (64x64, RGB with white background)
├── cat/                  # Cat pet type
│   ├── idle/             # Idle animation frames
│   │   ├── idle_00.png
│   │   ├── idle_01.png
│   │   └── ...
│   ├── walk/             # Walk animation frames
│   │   ├── walk_00.png
│   │   └── ...
│   ├── sleep/
│   ├── eat/
│   └── play/
├── dog/                  # Dog pet type (same structure)
│   └── ...
└── default/              # Default pet (fallback)
    └── ...
```

### Naming Convention

**File format:** `<action>_<frame_number>.png`

- `<action>`: lowercase action name (e.g., `idle`, `walk`, `sleep`)
- `<frame_number>`: zero-padded 2-digit number (e.g., `00`, `01`, `15`)

**Examples:**
- `idle_00.png`, `idle_01.png`, ..., `idle_15.png`
- `walk_00.png`, `walk_01.png`, ..., `walk_19.png`
- `dance_00.png` (custom action)

### Requirements & Restrictions

| Item | Requirement |
|------|-------------|
| **Format** | PNG with alpha channel (transparent background) |
| **Background** | Transparent or white (for tray icon compatibility) |
| **Minimum frames** | At least 1 frame required (`_00.png`) |
| **Naming** | Must match `<action>_<frame>.png` pattern exactly |
| **Action name** | Lowercase letters, numbers, underscores only |

### Adding a New Pet Type

1. Create a new directory under `resources/pets/`:
   ```
   resources/pets/fox/
   ```

2. Add action directories with sprite frames:
   ```
   resources/pets/fox/
   ├── idle/
   │   └── idle_00.png, idle_01.png, ...
   ├── walk/
   │   └── walk_00.png, walk_01.png, ...
   └── ...
   ```

3. The pet type name (`fox`) will automatically appear in the tray menu under "Pets"

### Adding a New Action

1. Create an action directory inside the pet folder:
   ```
   resources/pets/cat/dance/
   ```

2. Add sprite frames:
   ```
   resources/pets/cat/dance/
   ├── dance_00.png
   ├── dance_01.png
   ├── dance_02.png
   └── ...
   ```

3. The action (`dance`) will automatically appear in the tray menu under "Actions"

4. (Optional) Add command aliases in `deskpet/commands/__init__.py` for the new action

### Generating Test Sprites

Generate placeholder sprites for development:

```bash
python scripts/generate_sprites.py
```

### Windows Tray Icon Limitation

On Windows, the system tray does not support transparent PNG backgrounds. The tray icon (`resources/pets/icon.png`) must use a **white background** instead of transparency. Use the included logo generator:

```bash
python scripts/generate_logo.py
```

## Extending Chat System

Implement `ChatHandler` protocol for natural language responses:

```python
from deskpet.chat.base import ChatHandler
from deskpet.chat.registry import get_registry

class AIDemoHandler:
    def handle(self, message: str, context: dict) -> str:
        return "AI response here"

    def is_available(self) -> bool:
        return True

get_registry().register(AIDemoHandler())
```

## Configuration

Config auto-saves to `%USERPROFILE%\.deskpet\config.json`:

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
  }
}
```

Logs output to `log/deskpet.log` (cleared on each run).

## Development

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -e ".[dev]"
ruff check .
```

## Build

```bash
pyinstaller deskpet.spec --clean
```

Output: `dist/DeskPet/`

## License

MIT
