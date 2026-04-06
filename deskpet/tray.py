"""System tray icon and menu management."""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from deskpet.pet.engine import Behavior, PetEngine

import pystray
from PIL import Image


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
        self._icon: pystray.Icon | None = None
        self._pet_engine: "PetEngine | None" = None
        self._pet_types: list[str] = []
        self._on_switch_pet: Callable[[str], None] | None = None

    def set_pet_engine(self, engine: "PetEngine") -> None:
        self._pet_engine = engine

    def set_on_switch_pet(self, callback: Callable[[str], None]) -> None:
        self._on_switch_pet = callback

    def setup_menu(self, pet_types: list[str]) -> None:
        self._pet_types = pet_types

    def run(self) -> None:
        menu_items = self._build_menu()
        menu = pystray.Menu(*menu_items)

        try:
            image = Image.open(self.icon_path)
        except FileNotFoundError:
            image = Image.new("RGB", (64, 64), color="white")

        self._icon = pystray.Icon("deskpet", image, self.tooltip, menu)
        self._icon.run()

    def _build_menu(self) -> list[pystray.MenuItem]:
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

        menu_items: list[pystray.MenuItem | pystray.Menu] = [
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

    def _quit(self, icon: pystray.Icon | None = None) -> None:
        if self.on_quit:
            self.on_quit()
        self.stop()

    def stop(self) -> None:
        if self._icon:
            self._icon.stop()
            self._icon = None

    def update_menu(self) -> None:
        if self._icon:
            menu_items = self._build_menu()
            self._icon.menu = pystray.Menu(*menu_items)
