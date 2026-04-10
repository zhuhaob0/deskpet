"""System tray icon and menu management using PyQt6."""

from __future__ import annotations

import logging
import os
import threading
from typing import TYPE_CHECKING, Callable

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

if TYPE_CHECKING:
    from deskpet.pet.engine import Behavior, PetEngine

logger = logging.getLogger(__name__)


def _is_gui_available():
    """Check if GUI environment is available."""
    if os.name == "nt":
        try:
            import ctypes

            user32 = ctypes.windll.user32
            return user32.GetSystemMetrics(0) > 0 and user32.GetSystemMetrics(1) > 0
        except Exception:
            return False
    return True


class TrayManager:
    def __init__(
        self,
        icon_path: str,
        tooltip: str = "DeskPet",
        on_quit: Callable[[], None] | None = None,
        qapp: QApplication | None = None,
    ):
        self.icon_path = icon_path
        self.tooltip = tooltip
        self.on_quit = on_quit
        self._qapp = qapp
        self._tray: QSystemTrayIcon | None = None
        self._menu: QMenu | None = None
        self._pet_engine: "PetEngine | None" = None
        self._pet_types: list[str] = []
        self._on_switch_pet: Callable[[str], None] | None = None

    @property
    def is_available(self) -> bool:
        return QSystemTrayIcon.isSystemTrayAvailable()

    def set_pet_engine(self, engine: "PetEngine") -> None:
        self._pet_engine = engine

    def set_on_switch_pet(self, callback: Callable[[str], None]) -> None:
        self._on_switch_pet = callback

    def setup_menu(self, pet_types: list[str]) -> None:
        self._pet_types = pet_types

    def run(self) -> None:
        logger.info("TrayManager.run() starting...")

        gui_ok = _is_gui_available()
        logger.info(f"GUI available: {gui_ok}")

        if not gui_ok:
            logger.warning("No GUI environment detected, using console mode")
            self._run_console_mode()
            return

        app = self._qapp
        logger.info(f"QApplication instance: {app}")

        if app is None:
            logger.error("QApplication is None, cannot create tray")
            self._run_console_mode()
            return

        logger.info("Creating menu...")
        self._menu = QMenu()
        self._build_menu()
        logger.info("Menu created")

        logger.info("Creating QSystemTrayIcon...")
        from PyQt6.QtGui import QPixmap, QIcon

        try:
            pixmap = QPixmap(self.icon_path)
            if not pixmap.isNull():
                icon = QIcon(pixmap)
                self._tray = QSystemTrayIcon(icon, app)
                logger.info(f"Tray icon loaded from: {self.icon_path}")
            else:
                self._tray = QSystemTrayIcon(app)
                logger.warning("Failed to load tray icon, using default")
        except Exception as e:
            self._tray = QSystemTrayIcon(app)
            logger.warning(f"Failed to load tray icon: {e}")

        self._tray.setToolTip(self.tooltip)
        self._tray.setContextMenu(self._menu)
        self._tray.activated.connect(self._on_tray_activated)
        self._tray.show()
        logger.info("QSystemTrayIcon created and shown")

        logger.info("Running Qt event loop...")
        app.exec()
        logger.info("Qt event loop ended")

    def _on_tray_activated(self, reason) -> None:
        if int(reason) == QSystemTrayIcon.ActivationReason.DoubleClick:
            logger.info("Tray double-clicked")
            self._send_command("status")

    def _build_menu(self) -> None:
        if not self._menu:
            return

        self._menu.clear()

        walk_action = QAction("Walk Around", self._menu)
        walk_action.triggered.connect(lambda: self._send_command("walk"))
        self._menu.addAction(walk_action)

        sleep_action = QAction("Sleep", self._menu)
        sleep_action.triggered.connect(lambda: self._send_command("sleep"))
        self._menu.addAction(sleep_action)

        eat_action = QAction("Eat", self._menu)
        eat_action.triggered.connect(lambda: self._send_command("eat"))
        self._menu.addAction(eat_action)

        play_action = QAction("Play", self._menu)
        play_action.triggered.connect(lambda: self._send_command("play"))
        self._menu.addAction(play_action)

        self._menu.addSeparator()

        pets_menu = QMenu("Pets", self._menu)
        for pet_type in self._pet_types:
            pet_action = QAction(pet_type.title(), pets_menu)
            pet_action.triggered.connect(lambda checked, pt=pet_type: self._switch_pet(pt))
            pets_menu.addAction(pet_action)
        self._menu.addMenu(pets_menu)

        self._menu.addSeparator()

        quit_action = QAction("Quit", self._menu)
        quit_action.triggered.connect(self._quit)
        self._menu.addAction(quit_action)

    def _send_command(self, behavior_name: str) -> None:
        if self._pet_engine is None:
            return

        from deskpet.pet.engine import Behavior

        behavior_map = {
            "walk": ("walk", 0.0),
            "sleep": ("sleep", 8.0),
            "eat": ("eat", 3.0),
            "play": ("play", 6.0),
        }

        if behavior_name in behavior_map:
            cmd = behavior_map[behavior_name]
            if behavior_name == "walk":
                threading.Thread(target=self._pet_engine.walk_random, daemon=True).start()
            else:
                self._pet_engine.command(Behavior[cmd[0].upper()], cmd[1])

    def _switch_pet(self, pet_type: str) -> None:
        logger.info(f"Switching to pet: {pet_type}")
        if self._on_switch_pet:
            self._on_switch_pet(pet_type)

    def _quit(self) -> None:
        logger.info("Quit requested from tray")
        if self.on_quit:
            self.on_quit()
        self.stop()

    def stop(self) -> None:
        if self._tray:
            self._tray.hide()
            self._tray = None
        self._menu = None

    def _run_console_mode(self) -> None:
        print(f"\n{'=' * 50}")
        print(f"DeskPet Console Mode (tray not available)")
        print(f"{'=' * 50}")
        print(f"Pet: {self._pet_types[0] if self._pet_types else 'default'}")
        print(f"\nCommands:")
        print(f"  walk    - Random walk")
        print(f"  sleep   - Sleep for 8s")
        print(f"  eat     - Eat for 3s")
        print(f"  play    - Play for 6s")
        print(f"  status  - Show pet status")
        print(f"  quit    - Exit")
        print(f"{'=' * 50}\n")

        while True:
            try:
                cmd = input("> ").strip().lower()
                if cmd == "quit":
                    if self.on_quit:
                        self.on_quit()
                    break
                elif cmd in ("walk", "sleep", "eat", "play", "status"):
                    if cmd == "status" and self._pet_engine:
                        state = self._pet_engine.get_state()
                        print(f"  Behavior: {state.behavior.name}")
                        print(f"  Position: ({state.position_x}, {state.position_y})")
                    else:
                        self._send_command(cmd)
                elif cmd:
                    print(f"Unknown command: {cmd}")
            except (EOFError, KeyboardInterrupt):
                if self.on_quit:
                    self.on_quit()
                break
