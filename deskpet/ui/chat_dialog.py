"""Chat dialog UI using PyQt6."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


if TYPE_CHECKING:
    from deskpet.commands.base import CommandRegistry
    from deskpet.pet.engine import PetEngine


class ChatMessage:
    def __init__(
        self, text: str, is_user: bool, is_command: bool = False, timestamp: datetime | None = None
    ):
        self.text = text
        self.is_user = is_user
        self.is_command = is_command
        self.timestamp = timestamp or datetime.now()


class ChatBubble(QWidget):
    def __init__(self, message: ChatMessage, parent: QWidget | None = None):
        super().__init__(parent)
        self.message = message
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(2)

        time_label = QLabel(self.message.timestamp.strftime("%H:%M"))
        time_label.setStyleSheet("color: #888; font-size: 10px;")

        content_label = QLabel(self.message.text)
        content_label.setWordWrap(True)
        content_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        if self.message.is_user:
            bubble_style = """
                background-color: #0078D4;
                color: white;
                border-radius: 12px;
                padding: 8px 12px;
            """
            time_style = "color: #6699cc; font-size: 10px;"
        else:
            if self.message.is_command:
                bubble_style = """
                    background-color: #2d2d2d;
                    color: #00ff00;
                    border-radius: 12px;
                    padding: 8px 12px;
                    font-family: Consolas, monospace;
                """
            else:
                bubble_style = """
                    background-color: #3a3a3a;
                    color: white;
                    border-radius: 12px;
                    padding: 8px 12px;
                """
            time_style = "color: #888; font-size: 10px;"

        time_label.setStyleSheet(time_style)
        content_label.setStyleSheet(bubble_style)

        layout.addWidget(time_label, 0, Qt.AlignmentFlag.AlignRight)
        layout.addWidget(
            content_label,
            0,
            Qt.AlignmentFlag.AlignRight if self.message.is_user else Qt.AlignmentFlag.AlignLeft,
        )


class ChatDialog(QDialog):
    def __init__(
        self,
        pet_name: str = "Pet",
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self.pet_name = pet_name
        self._messages: list[ChatMessage] = []

        self._command_registry = None
        self._pet_engine: PetEngine | None = None
        self._chat_registry = None

        self.setup_ui()
        self.setWindowTitle(f"Chat with {pet_name}")

    def set_dependencies(
        self,
        command_registry: "CommandRegistry",
        pet_engine: "PetEngine",
        chat_registry,
    ) -> None:
        self._command_registry = command_registry
        self._pet_engine = pet_engine
        self._chat_registry = chat_registry

    def setup_ui(self) -> None:
        self.setMinimumSize(400, 500)
        self.setMaximumSize(600, 700)
        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.WindowCloseButtonHint
            | Qt.WindowType.WindowMinimizeButtonHint
        )

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("#1e1e1e"))
        self.setPalette(palette)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        header = self._create_header()
        main_layout.addWidget(header)

        self.chat_area = self._create_chat_area()
        main_layout.addWidget(self.chat_area, 1)

        input_area = self._create_input_area()
        main_layout.addWidget(input_area)

        self._add_welcome_message()

    def _create_header(self) -> QWidget:
        header = QWidget()
        header.setStyleSheet("background-color: #2d2d2d; border-bottom: 1px solid #444;")
        header.setFixedHeight(50)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(16, 0, 16, 0)

        title = QLabel(f"  {self.pet_name}")
        title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        title.setStyleSheet("color: white; background: transparent;")

        help_btn = QPushButton("?")
        help_btn.setFixedSize(28, 28)
        help_btn.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: white;
                border: none;
                border-radius: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        help_btn.clicked.connect(self._show_help)

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(help_btn)

        return header

    def _create_chat_area(self) -> QWidget:
        container = QWidget()
        container.setStyleSheet("background-color: #1e1e1e;")

        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #333;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle {
                background-color: #555;
                border-radius: 4px;
            }
            QScrollBar::handle:hover {
                background-color: #666;
            }
        """)

        self.messages_widget = QWidget()
        self.messages_layout = QVBoxLayout(self.messages_widget)
        self.messages_layout.setContentsMargins(0, 0, 0, 0)
        self.messages_layout.setSpacing(8)
        self.messages_layout.addStretch()

        scroll.setWidget(self.messages_widget)
        layout.addWidget(scroll)

        return container

    def _create_input_area(self) -> QWidget:
        input_widget = QWidget()
        input_widget.setStyleSheet("background-color: #2d2d2d; border-top: 1px solid #444;")

        layout = QHBoxLayout(input_widget)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type a message or /command...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #3a3a3a;
                color: white;
                border: none;
                border-radius: 18px;
                padding: 10px 16px;
                font-size: 13px;
            }
            QLineEdit:focus {
                background-color: #404040;
            }
            QLineEdit::placeholder {
                color: #888;
            }
        """)
        self.input_field.returnPressed.connect(self._on_send)
        self.input_field.textChanged.connect(self._on_text_changed)

        self.send_btn = QPushButton("Send")
        self.send_btn.setFixedSize(70, 36)
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078D4;
                color: white;
                border: none;
                border-radius: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1a86d9;
            }
            QPushButton:pressed {
                background-color: #006cbd;
            }
        """)
        self.send_btn.clicked.connect(self._on_send)

        layout.addWidget(self.input_field, 1)
        layout.addWidget(self.send_btn)

        return input_widget

    def _add_welcome_message(self) -> None:
        welcome = f"""Hi! I'm {self.pet_name}.

I can understand commands starting with /:
  /walk [x y]  - Walk to position or randomly
  /sleep [sec] - Take a nap
  /eat          - Have a snack
  /play         - Have fun
  /status       - Check my status
  /help         - Show all commands

You can also just chat with me!"""

        self._add_message(ChatMessage(welcome, is_user=False))

    def _add_message(self, message: ChatMessage) -> None:
        self._messages.append(message)

        bubble = ChatBubble(message)
        self.messages_layout.insertWidget(self.messages_layout.count() - 1, bubble)

        self._scroll_to_bottom()

    def _scroll_to_bottom(self) -> None:
        scroll_area = self.chat_area.findChild(QScrollArea)
        if scroll_area:
            scroll_area.verticalScrollBar().setValue(scroll_area.verticalScrollBar().maximum())

    def _on_text_changed(self, text: str) -> None:
        if text.startswith("/"):
            self._show_command_hint(text)
        else:
            self.send_btn.setEnabled(bool(text.strip()))

    def _show_command_hint(self, text: str) -> None:
        self.send_btn.setEnabled(bool(text.strip()))

    def _show_help(self) -> None:
        help_text = """Commands:
  /walk [x y]     - Walk to coordinates or random
  /walk random    - Walk to random position
  /sleep [sec]    - Sleep (default 8s)
  /eat [sec]      - Eat (default 3s)  
  /play [sec]     - Play (default 6s)
  /status         - Show pet status
  /config <key> <val> - Change settings
  /help [cmd]     - Show this help

You can also chat with me normally!"""
        self._add_message(ChatMessage(help_text, is_user=False))

    def _on_send(self) -> None:
        text = self.input_field.text().strip()
        if not text:
            return

        self.input_field.clear()

        is_command = text.startswith("/")
        self._add_message(ChatMessage(text, is_user=True, is_command=is_command))

        if is_command:
            self._execute_command(text)
        else:
            self._handle_chat(text)

    def _execute_command(self, text: str) -> None:
        if self._command_registry is None or self._pet_engine is None:
            self._add_message(ChatMessage("System not ready", is_user=False))
            return

        from deskpet.commands.base import CommandContext

        context = CommandContext(pet_engine=self._pet_engine, user_data={})
        result = self._command_registry.execute(text, context)

        if result.success:
            self._add_message(ChatMessage(result.message, is_user=False, is_command=True))
        else:
            self._add_message(
                ChatMessage(f"Error: {result.message}", is_user=False, is_command=True)
            )

    def _handle_chat(self, text: str) -> None:
        if self._chat_registry is None:
            response = "I'm not sure how to respond right now."
            self._add_message(ChatMessage(response, is_user=False))
            return

        context = {"message": text}
        response = self._chat_registry.send(text, context)

        if response:
            self._add_message(ChatMessage(response, is_user=False))
        else:
            self._add_message(
                ChatMessage("I didn't understand that. Try /help for commands.", is_user=False)
            )

    def closeEvent(self, event) -> None:
        event.accept()
