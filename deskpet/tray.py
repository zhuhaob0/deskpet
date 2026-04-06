"""System tray icon and menu management."""

from __future__ import annotations

import logging
import platform
import sys
import threading
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from deskpet.pet.engine import Behavior, PetEngine

logger = logging.getLogger(__name__)

_pystray_available = False


def _check_pystray():
    global _pystray_available
    if _pystray_available:
        return True
    try:
        import pystray as _pyst
        from PIL import Image
        globals()['pystray'] = _pyst
        globals()['Image'] = Image
        _pystray_available = True
        return True
    except (ImportError, ValueError, Exception) as e:
        logger.warning(f"pystray not available: {e}")
        return False


class TrayManager:
    def __init__(
        self,
        icon_path: str,
        tooltip: str = "DeskPet",
        on_quit: Callable[[], None] | None = None,
    ):
        self.icon_path = icon_path
        self.tooltip = tooltip
        self.on_quit = on_quit
        self._icon = None
        self._pet_engine: "PetEngine | None" = None
        self._pet_types: list[str] = []
        self._on_switch_pet: Callable[[str], None] | None = None

    @property
    def is_available(self) -> bool:
        return _pystray_available

    def set_pet_engine(self, engine: "PetEngine") -> None:
        self._pet_engine = engine

    def set_on_switch_pet(self, callback: Callable[[str], None]) -> None:
        self._on_switch_pet = callback

    def setup_menu(self, pet_types: list[str]) -> None:
        self._pet_types = pet_types

    def run(self) -> None:
        if not _check_pystray():
            logger.warning("System tray not available on this platform")
            self._run_console_mode()
            return

        menu_items = self._build_menu()
        menu = pystray.Menu(*menu_items)

        try:
            image = Image.open(self.icon_path)
        except FileNotFoundError:
            image = Image.new("RGB", (64, 64), color="white")

        self._icon = pystray.Icon("deskpet", image, self.tooltip, menu)
        self._icon.run()

    def _run_console_mode(self) -> None:
        print(f"\n{'='*50}")
        print(f"DeskPet Console Mode (pystray not available)")
        print(f"{'='*50}")
        print(f"Pet: {self._pet_types[0] if self._pet_types else 'default'}")
        print(f"\nCommands:")
        print(f"  walk    - Random walk")
        print(f"  sleep   - Sleep for 8s")
        print(f"  eat     - Eat for 3s")
        print(f"  play    - Play for 6s")
        print(f"  status  - Show pet status")
        print(f"  quit    - Exit")
        print(f"{'='*50}\n")

        while True:
            try:
                cmd = input("> ").strip().lower()
                if cmd == "quit":
                    if self.on_quit:
                        self.on_quit()
                    break
                elif cmd in ("walk", "sleep", "eat", "play", "status"):
                    self._handle_console_command(cmd)
                elif cmd:
                    print(f"Unknown command: {cmd}")
            except (EOFError, KeyboardInterrupt):
                if self.on_quit:
                    self.on_quit()
                break

    def _handle_console_command(self, cmd: str) -> None:
        if cmd == "status" and self._pet_engine:
            state = self._pet_engine.get_state()
            print(f"  Behavior: {state.behavior.name}")
            print(f"  Position: ({state.position_x}, {state.position_y})")
        else:
            self._send_command(cmd)

    def _build_menu(self) -> list:
        behavior_items = [
            pystray.MenuItem(
                "Walk Around",
                lambda _: self._send_command("walk"),
                default=False,
            ),
            pystray.MenuItem(
                "Sleep",
                lambda _: self._send_command("sleep"),
                default=False,
            ),
            pystray.MenuItem(
                "Eat",
                lambda _: self._send_command("eat"),
                default=False,
            ),
            pystray.MenuItem(
                "Play",
                lambda _: self._send_command("play"),
                default=False,
            ),
        ]

        pet_items = []
        for pet_type in self._pet_types:
            pet_items.append(
                pystray.MenuItem(
                    f"Switch to {pet_type.title()}",
                    lambda _, pt=pet_type: self._switch_pet(pt),
                    default=False,
                )
            )

        menu_items = [
            pystray.MenuItem("Behaviors", pystray.Menu(*behavior_items)),
            pystray.MenuItem("Pets", pystray.Menu(*pet_items)),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self._quit, default=True),
        ]

        return menu_items

    def _send_command(self, behavior_name: str) -> None:
        if self._pet_engine is None:
            return

        behavior_map = {
            "walk": (self._pet_engine.walk_random, 0.0),
            "sleep": ("sleep", 8.0),
            "eat": ("eat", 3.0),
            "play": ("play", 6.0),
        }

        if behavior_name in behavior_map:
            cmd = behavior_map[behavior_name]
            if callable(cmd[0]):
                threading.Thread(target=cmd[0], daemon=True).start()
            else:
                from deskpet.pet.engine import Behavior
                self._pet_engine.command(Behavior[behavior_name.upper()], cmd[1])

    def _switch_pet(self, pet_type: str) -> None:
        if self._on_switch_pet:
            self._on_switch_pet(pet_type)

    def _quit(self, icon=None) -> None:
        if self.on_quit:
            self.on_quit()
        self.stop()

    def stop(self) -> None:
        if self._icon:
            self._icon.stop()
            self._icon = None
