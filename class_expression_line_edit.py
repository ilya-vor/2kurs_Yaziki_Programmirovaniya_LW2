from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class ExpressionLineEdit(QLineEdit):
    def __init__(self, parent, x: int, y: int, w: int, h: int):
        super().__init__(parent)
        if w < 0 or h < 0:
            raise Exception(f"[ERROR] Недопустимый размер")

        self.__initUI(x, y, w, h)

    def error(self):
        self.setStyleSheet(
            """
                color: rgb(178, 34, 34);
                border-radius: 5px;
            """
        )
        self.clearFocus()

    def success(self):
        self.setStyleSheet(
            """
                color: rgb(34, 139, 34);
                border-radius: 5px;
            """
        )

    def finish(self):
        expression_in = self.text()
        self.clearFocus()

        return expression_in

    def mousePressEvent(self, a0):
        super().mousePressEvent(a0)
        self.setStyleSheet(
            """
                border-radius: 5px;
            """
        )

    def __initUI(self, x: int, y: int, w: int, h: int):
        font = QFont()
        font.setPointSize(15)
        self.setFont(font)
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.setFixedSize(w, h)
        self.move(x, y)
        self.setStyleSheet(
            """
                border-radius: 5px;
            """
        )
