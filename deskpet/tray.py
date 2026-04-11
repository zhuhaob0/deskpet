"""System tray icon and menu management using PyQt6."""

from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING, Callable

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

if TYPE_CHECKING:
    from deskpet.pet.engine import PetEngine
    from deskpet.utils.sprite_importer import SpriteImporter

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


SELECTED_STYLE = "background-color: #4a90d9; color: white;"
DEFAULT_STYLE = ""


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
        self._sprite_importer: "SpriteImporter | None" = None
        self._current_pet: str = ""
        self._current_behavior: str = "idle"

    @property
    def is_available(self) -> bool:
        return QSystemTrayIcon.isSystemTrayAvailable()

    def set_pet_engine(self, engine: "PetEngine") -> None:
        self._pet_engine = engine

    def set_on_switch_pet(self, callback: Callable[[str], None]) -> None:
        self._on_switch_pet = callback

    def set_sprite_importer(self, importer: "SpriteImporter") -> None:
        self._sprite_importer = importer

    def setup_menu(self, pet_types: list[str]) -> None:
        self._pet_types = pet_types

    def refresh_menu(self) -> None:
        if self._sprite_importer:
            self._pet_types = self._sprite_importer.get_available_pets()
            logger.info(f"Refreshed pet types: {self._pet_types}")
        self._build_menu()

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
        from PyQt6.QtGui import QPixmap

        try:
            pixmap = QPixmap(self.icon_path)
            if not pixmap.isNull():
                icon = QIcon()
                icon.addPixmap(pixmap, QIcon.Mode.Normal)
                self._tray = QSystemTrayIcon(app)
                self._tray.setIcon(icon)
                logger.info(f"Tray icon loaded from: {self.icon_path}, size: {pixmap.size()}")
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
        from PyQt6.QtWidgets import QSystemTrayIcon

        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            logger.info("Tray double-clicked")
            self._send_command("status")

    def _build_menu(self) -> None:
        if not self._menu:
            return

        self._menu.clear()

        pet_types = self._get_all_pet_types()
        pets_menu = QMenu("Pets", self._menu)
        for pet_type in pet_types:
            is_selected = pet_type == self._current_pet
            pet_action = QAction(("✓ " if is_selected else "") + pet_type.title(), pets_menu)
            pet_action.setStyleSheet(SELECTED_STYLE if is_selected else DEFAULT_STYLE)
            pet_action.triggered.connect(lambda checked, pt=pet_type: self._switch_pet(pt))
            pets_menu.addAction(pet_action)
        self._menu.addMenu(pets_menu)
        self._menu.addSeparator()

        behaviors = self._get_available_behaviors()
        if behaviors:
            actions_menu = QMenu("Actions", self._menu)
            for behavior in behaviors:
                is_selected = behavior == self._current_behavior
                action = QAction(("✓ " if is_selected else "") + behavior.title(), actions_menu)
                action.setStyleSheet(SELECTED_STYLE if is_selected else DEFAULT_STYLE)
                action.triggered.connect(lambda checked, b=behavior: self._send_command(b))
                actions_menu.addAction(action)
            self._menu.addMenu(actions_menu)

        self._menu.addSeparator()

        import_action = QAction("Import Animation...", self._menu)
        import_action.triggered.connect(self._open_import_dialog)
        self._menu.addAction(import_action)

        self._menu.addSeparator()

        quit_action = QAction("Quit", self._menu)
        quit_action.triggered.connect(self._quit)
        self._menu.addAction(quit_action)

    def _get_all_pet_types(self) -> list[str]:
        if self._sprite_importer:
            return self._sprite_importer.get_available_pets()
        return self._pet_types

    def _get_available_behaviors(self) -> list[str]:
        if self._sprite_importer and self._current_pet:
            return self._sprite_importer.get_available_actions(self._current_pet)
        if self._pet_engine:
            return self._pet_engine.get_available_behaviors()
        return ["idle", "walk", "sleep", "eat", "play"]

    def _open_import_dialog(self) -> None:
        if not self._sprite_importer:
            logger.warning("Sprite importer not set")
            return

        from deskpet.ui.import_dialog import ImportDialog

        dialog = ImportDialog(self._sprite_importer)
        if dialog.exec():
            logger.info("Import dialog accepted, refreshing menu")
            self.refresh_menu()

    def _send_command(self, behavior_name: str) -> None:
        logger.info(f"Command received: {behavior_name}")
        if self._pet_engine is None:
            logger.warning("Pet engine not initialized")
            return

        from deskpet.pet.engine import Behavior

        self._current_behavior = behavior_name

        if behavior_name == "walk":
            logger.info("Sending walk command")
            self._pet_engine.command(Behavior.WALK, 0.0)
            logger.info("Walk command sent successfully")
        elif behavior_name in ("sleep", "eat", "play"):
            duration_map = {"sleep": 8.0, "eat": 3.0, "play": 6.0}
            duration = duration_map.get(behavior_name, 5.0)
            logger.info(f"Sending {behavior_name} command, duration: {duration}")
            self._pet_engine.command(Behavior[behavior_name.upper()], duration)
            logger.info(f"{behavior_name} command sent successfully")
        else:
            logger.info(f"Sending {behavior_name} command")
            try:
                self._pet_engine.command(Behavior[behavior_name.upper()], 5.0)
            except KeyError:
                logger.warning(f"Unknown behavior: {behavior_name}")

    def _switch_pet(self, pet_type: str) -> None:
        logger.info(f"Switching to pet: {pet_type}")
        self._current_pet = pet_type

        if self._on_switch_pet:
            self._on_switch_pet(pet_type)

        behaviors = (
            self._sprite_importer.get_available_actions(pet_type) if self._sprite_importer else []
        )
        if behaviors:
            default_action = behaviors[0]
            self._current_behavior = default_action
            logger.info(f"Triggering default action for {pet_type}: {default_action}")
            self._send_command(default_action)

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
        print("DeskPet Console Mode (tray not available)")
        print(f"{'=' * 50}")
        print(f"Pet: {self._pet_types[0] if self._pet_types else 'default'}")
        print("\nCommands:")
        print("  walk    - Random walk")
        print("  sleep   - Sleep for 8s")
        print("  eat     - Eat for 3s")
        print("  play    - Play for 6s")
        print("  status  - Show pet status")
        print("  quit    - Exit")
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
