"""Import dialog for sprite animation from GIF/MP4."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

if TYPE_CHECKING:
    from deskpet.utils.sprite_importer import SpriteImporter

logger = logging.getLogger(__name__)


class ImportDialog(QDialog):
    def __init__(self, importer: "SpriteImporter", parent=None):
        super().__init__(parent)
        self.importer = importer
        self.selected_file = ""

        self.setWindowTitle("Import Sprite Animation")
        self.setModal(True)
        self.setMinimumWidth(450)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        file_layout = QHBoxLayout()
        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Select GIF or MP4 file...")
        self.file_input.setReadOnly(True)
        file_layout.addWidget(QLabel("File:"))
        file_layout.addWidget(self.file_input)

        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self._browse_file)
        file_layout.addWidget(browse_btn)
        layout.addLayout(file_layout)

        pet_layout = QHBoxLayout()
        pet_layout.addWidget(QLabel("Pet Name:"))
        self.pet_input = QComboBox()
        self.pet_input.setEditable(True)
        self._refresh_pet_list()
        pet_layout.addWidget(self.pet_input)
        layout.addLayout(pet_layout)

        action_layout = QHBoxLayout()
        action_layout.addWidget(QLabel("Action Name:"))
        self.action_input = QLineEdit()
        self.action_input.setPlaceholderText("e.g., idle, walk, dance...")
        action_layout.addWidget(self.action_input)
        layout.addLayout(action_layout)

        info_label = QLabel(
            "The animation will be extracted at 30 FPS.\n"
            "Frames will be saved as: {pet}/{action}/{action}_00.png"
        )
        info_label.setStyleSheet("color: gray; font-size: 11px;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        self.import_btn = QPushButton("Import")
        self.import_btn.clicked.connect(self._do_import)
        btn_layout.addWidget(self.import_btn)

        layout.addLayout(btn_layout)

    def _refresh_pet_list(self) -> None:
        self.pet_input.clear()
        self.pet_input.addItem("")
        self.pet_input.addItems(self.importer.get_available_pets())

    def _browse_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Animation File",
            "",
            "Media Files (*.gif *.mp4 *.avi *.mkv *.mov *.wmv);;All Files (*)",
        )
        if file_path:
            self.selected_file = file_path
            self.file_input.setText(file_path)

            path = Path(file_path)
            suggested_action = path.stem.lower().replace(" ", "_").replace("-", "_")
            self.action_input.setText(suggested_action)

    def _do_import(self) -> None:
        if not self.selected_file:
            self.file_input.setFocus()
            return

        pet_name = self.pet_input.currentText().strip()
        if not pet_name:
            self.pet_input.setFocus()
            return

        action_name = self.action_input.text().strip()
        if not action_name:
            self.action_input.setFocus()
            return

        self.import_btn.setEnabled(False)
        self.import_btn.setText("Importing...")

        success, message = self.importer.import_from_file(self.selected_file, pet_name, action_name)

        self.import_btn.setEnabled(True)
        self.import_btn.setText("Import")

        if success:
            logger.info(f"Import successful: {message}")
            self.accept()
        else:
            logger.error(f"Import failed: {message}")
            self.action_input.selectAll()
            self.action_input.setFocus()
