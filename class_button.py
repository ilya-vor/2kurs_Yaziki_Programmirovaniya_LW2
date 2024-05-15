from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import pyqtSlot


class Button(QPushButton):
    def __init__(self, parent, x: int, y: int, w: int, h: int, text: str, slot: pyqtSlot):
        super().__init__(parent)
        if w < 0 or h < 0:
            raise Exception(f"[ERROR] Недопустимый размер")

        self.clicked.connect(slot)

        self.__initUI(x, y, w, h, text)

    def __initUI(self, x: int, y: int, w: int, h: int, text: str):
        self.setFixedSize(w, h)
        self.move(x, y)
        self.setStyleSheet(
            """
                border-radius: 5px;
                font: 12pt;
            """
        )
        self.setText(text)
