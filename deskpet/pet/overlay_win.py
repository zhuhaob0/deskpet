"""Windows-specific transparent overlay using PyQt6."""

from __future__ import annotations

import logging
from PyQt6.QtCore import Qt, QPoint, QRect
from PyQt6.QtGui import QPixmap, QMouseEvent, QPainter, QRegion
from PyQt6.QtWidgets import QLabel, QWidget

from deskpet.pet.overlay import PetOverlay

logger = logging.getLogger(__name__)


class TransparentWindow(QWidget):
    def __init__(self, on_double_click=None, on_position_changed=None):
        super().__init__()
        self._on_double_click = on_double_click
        self._on_position_changed = on_position_changed
        self._drag_start = None
        self._is_dragging = False
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setFixedSize(128, 128)
        self.setMouseTracking(True)

        self._label = QLabel(self)
        self._label.setFixedSize(128, 128)
        self._label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._label.setStyleSheet("background: transparent;")

    def set_pixmap(self, path: str) -> None:
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            scaled = pixmap.scaled(
                128,
                128,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self._label.setPixmap(scaled)
            self.setMask(scaled.mask())

    @property
    def is_dragging(self) -> bool:
        return self._is_dragging

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start = event.globalPosition().toPoint()
            self._is_dragging = True
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._is_dragging and self._drag_start:
            delta = event.globalPosition().toPoint() - self._drag_start
            new_pos = self.pos() + delta
            self.move(new_pos)
            self._drag_start = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self._on_position_changed:
            self._on_position_changed(self.pos().x(), self.pos().y())
        self._drag_start = None
        self._is_dragging = False
        event.accept()

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if self._on_double_click:
            self._on_double_click()
        event.accept()


class WindowsOverlay(PetOverlay):
    def __init__(self, on_double_click=None, on_position_changed=None):
        super().__init__(on_double_click)
        self._app = None
        self._window: TransparentWindow | None = None
        self._on_position_changed = on_position_changed

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
            self._window = TransparentWindow(
                on_double_click=self.on_double_click, on_position_changed=self._on_position_changed
            )

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
