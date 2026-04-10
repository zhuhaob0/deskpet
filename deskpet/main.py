"""DeskPet main entry point."""

from __future__ import annotations

import json
import logging
import os
import sys
import threading
import time
from pathlib import Path
from typing import TYPE_CHECKING

from deskpet.chat import get_registry, StaticChatHandler
from deskpet.commands.base import get_command_registry
from deskpet.config import AppConfig
from deskpet.pet import Behavior, PetEngine
from deskpet.pet.engine import ScreenBounds
from deskpet.pet.overlay import PetOverlay
from deskpet.tray import TrayManager

if TYPE_CHECKING:
    from deskpet.ui import ChatDialog


def get_log_dir() -> Path:
    if getattr(sys, "frozen", False):
        base = Path(sys._MEIPASS).parent
    else:
        base = Path(__file__).parent.parent
    log_dir = base / "log"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def clear_log_dir(log_dir: Path) -> None:
    for log_file in log_dir.glob("*.log"):
        log_file.unlink(missing_ok=True)


def setup_logging() -> None:
    log_dir = get_log_dir()
    clear_log_dir(log_dir)
    log_file = log_dir / "deskpet.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Set PIL logging to WARNING to reduce noise
    logging.getLogger("PIL").setLevel(logging.WARNING)

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )

    logging.getLogger().addHandler(file_handler)

    logging.info(f"Log file: {log_file}")


logger = logging.getLogger(__name__)


def get_resource_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / "resources"
    return Path(__file__).parent.parent / "resources"


def get_screen_size() -> tuple[int, int]:
    try:
        import ctypes

        user32 = ctypes.windll.user32
        return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    except Exception:
        return 1920, 1080


def load_responses(config: AppConfig) -> dict[str, str]:
    default_responses = {
        "hello": ["Hi there!", "Hello!", "Hey!"],
        "walk": ["Okay, I'll take a walk!", "Going for a stroll..."],
        "sleep": ["Time for a nap...", "Zzz..."],
        "eat": ["Yummy!", "Nom nom nom..."],
        "play": ["Wheee!", "This is fun!"],
        "bye": ["Bye bye!", "See you later!"],
    }

    if config.chat.responses_file:
        path = Path(config.chat.responses_file)
        if path.exists():
            with open(path) as f:
                return json.load(f)

    return default_responses


class ChatDialogController:
    def __init__(self, pet_engine: PetEngine, chat_registry, command_registry):
        self._pet_engine = pet_engine
        self._chat_registry = chat_registry
        self._command_registry = command_registry
        self._window: ChatDialog | None = None
        self._context: dict = {}

    def open(self) -> None:
        if self._window is None:
            self._window = self._create_window()
        self._window.show()
        self._window.activateWindow()
        self._window.raise_()

    def close(self) -> None:
        if self._window:
            self._window.close()
            self._window = None

    def _create_window(self) -> ChatDialog:
        from deskpet.ui import ChatDialog

        pet_name = self._pet_engine.get_state().name
        window = ChatDialog(pet_name=pet_name)
        window.set_dependencies(
            command_registry=self._command_registry,
            pet_engine=self._pet_engine,
            chat_registry=self._chat_registry,
        )
        return window


class DeskPetApp:
    def __init__(self):
        self.config = AppConfig.load()
        self.resource_dir = get_resource_dir()
        self.pet_engine: PetEngine | None = None
        self.overlay: PetOverlay | None = None
        self.tray: TrayManager | None = None
        self.chat_controller: ChatDialogController | None = None
        self._running = False
        self._update_thread: threading.Thread | None = None

    def initialize(self) -> None:
        screen_width, screen_height = get_screen_size()
        bounds = ScreenBounds(width=screen_width, height=screen_height)

        self.pet_engine = PetEngine(
            pet_type=self.config.pet.type,
            resource_dir=self.resource_dir / "pets",
            bounds=bounds,
        )
        self.pet_engine.start()

        self._setup_chat()
        self._setup_overlay()
        self._setup_tray()

    def _setup_chat(self) -> None:
        responses = load_responses(self.config)
        chat_handler = StaticChatHandler(responses)
        get_registry().register(chat_handler)

        self.chat_controller = ChatDialogController(
            pet_engine=self.pet_engine,
            chat_registry=get_registry(),
            command_registry=get_command_registry(),
        )

    def _setup_overlay(self) -> None:
        import platform

        system = platform.system().lower()
        if system == "windows":
            from deskpet.pet.overlay_win import WindowsOverlay

            self.overlay = WindowsOverlay(on_double_click=self._on_pet_double_click)
        else:
            from deskpet.pet.overlay_console import ConsoleOverlay

            self.overlay = ConsoleOverlay(on_double_click=self._on_pet_double_click)

    def _setup_tray(self) -> None:
        icon_path = str(self.resource_dir / "icon.png")
        self.tray = TrayManager(
            icon_path=icon_path,
            tooltip="DeskPet",
            on_quit=self.quit,
        )
        self.tray.set_pet_engine(self.pet_engine)
        self.tray.set_on_switch_pet(self._switch_pet)
        self.tray.setup_menu(["cat", "dog", "default"])

    def _on_pet_double_click(self) -> None:
        logger.info("Pet double-clicked - opening chat")
        if self.chat_controller:
            self.chat_controller.open()

    def _switch_pet(self, pet_type: str) -> None:
        logger.info(f"Switching to pet type: {pet_type}")
        self.config.pet.type = pet_type
        self.config.save()
        if self.pet_engine:
            self.pet_engine.stop()
            self.pet_engine = PetEngine(
                pet_type=pet_type,
                resource_dir=self.resource_dir / "pets",
                bounds=self.pet_engine.bounds,
            )
            self.pet_engine.start()
            if self.tray:
                self.tray.set_pet_engine(self.pet_engine)
            if self.chat_controller:
                self.chat_controller = ChatDialogController(
                    pet_engine=self.pet_engine,
                    chat_registry=get_registry(),
                    command_registry=get_command_registry(),
                )

    def _update_loop(self, fps: float = 30.0) -> None:
        frame_time = 1.0 / fps
        last_sprite = ""
        last_position = (0, 0)

        while self._running:
            if self.pet_engine and self.overlay:
                result = self.pet_engine.tick()

                if result.sprite != last_sprite:
                    self.overlay.update_sprite(result.sprite)
                    last_sprite = result.sprite

                if result.position != last_position:
                    self.overlay.move(result.position)
                    last_position = result.position

                if not self.overlay._window:
                    self.overlay.show(result.sprite, result.position)

            time.sleep(frame_time)

    def run(self) -> None:
        logger.info("DeskPet.run() starting...")
        self._running = True

        self._update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self._update_thread.start()
        logger.info("Update thread started")

        logger.info("Starting tray...")
        if self.tray:
            self.tray.run()
        logger.info("Tray.run() returned")

    def quit(self) -> None:
        logger.info("Shutting down DeskPet")
        self._running = False

        if self.chat_controller:
            self.chat_controller.close()

        if self.pet_engine:
            self.pet_engine.stop()

        if self.overlay:
            self.overlay.hide()

        if self.tray:
            self.tray.stop()

        sys.exit(0)


def main() -> None:
    setup_logging()
    logger.info("DeskPet starting...")

    try:
        app = DeskPetApp()
        app.initialize()
        app.run()
    except Exception as e:
        import traceback

        logger.exception("Fatal error in main")
        print(f"Fatal error: {e}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        input("Press Enter to exit...")  # 等待用户查看错误
        sys.exit(1)


if __name__ == "__main__":
    main()
