from PyQt6.QtWidgets import QLabel, QFrame
from PyQt6.QtCore import Qt


class Label(QLabel):
    def __init__(self, parent, x: int, y: int, w: int, h: int, r: int, g: int, b: int, text: str = None):
        super().__init__(parent)
        if w < 0 or h < 0:
            raise Exception(f"[ERROR] Недопустимый размер")

        if r > 255 or g > 255 or b > 255:
            raise Exception(f"[ERROR] Превышен допустимый диапазон для цвета")

        self.__initUI(x, y, w, h, r, g, b, text)

    def __initUI(self, x: int, y: int, w: int, h: int, r: int, g: int, b: int, text: str = None):
        self.setGeometry(x, y, w, h)
        self.setStyleSheet(
            f"""
                color: rgb({r}, {g}, {b});
                border: 1px solid rgb(0, 0, 0);
                border-radius: 5px;
                font: 15pt;
            """
        )
        self.setFrameStyle(QFrame.Shape.Box)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText(text)
