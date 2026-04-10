"""Windows-specific transparent overlay using PyQt6."""

from __future__ import annotations

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPixmap, QMouseEvent
from PyQt6.QtWidgets import QLabel, QWidget

from deskpet.pet.overlay import PetOverlay


class TransparentWindow(QWidget):
    def __init__(self, on_double_click=None):
        super().__init__()
        self._on_double_click = on_double_click
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setFixedSize(128, 128)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self._label = QLabel(self)
        self._label.setFixedSize(128, 128)
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def set_pixmap(self, path: str) -> None:
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            scaled = pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio)
            self._label.setPixmap(scaled)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if self._on_double_click:
            self._on_double_click()


class WindowsOverlay(PetOverlay):
    def __init__(self, on_double_click=None):
        super().__init__(on_double_click)
        self._app = None
        self._window: TransparentWindow | None = None

    def show(self, sprite_path: str, position: tuple[int, int]) -> None:
        from PyQt6.QtWidgets import QApplication
        import sys

        if self._app is None:
            try:
                self._app = QApplication.instance()
                if self._app is None:
                    self._app = QApplication(sys.argv)
                    logger = __import__("logging").getLogger(__name__)
                    logger.info("Created new QApplication")
            except RuntimeError as e:
                logger = __import__("logging").getLogger(__name__)
                logger.warning(f"QApplication already exists: {e}")
                self._app = QApplication.instance()

        if self._window is None:
            self._window = TransparentWindow(on_double_click=self.on_double_click)

        self._window.set_pixmap(sprite_path)
        self._window.move(QPoint(position[0], position[1]))
        self._window.show()

    def move(self, position: tuple[int, int]) -> None:
        if self._window:
            self._window.move(QPoint(position[0], position[1]))

    def update_sprite(self, sprite_path: str) -> None:
        if self._window:
            self._window.set_pixmap(sprite_path)

    def hide(self) -> None:
        if self._window:
            self._window.close()
            self._window = None

    def exec_(self) -> None:
        if self._app:
            self._app.exec()
