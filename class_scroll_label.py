from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QScrollArea
from class_label import Label


class ScrollLabel(QScrollArea):
    def __init__(self, parent, x: int, y: int, w: int, h: int, r: int, g: int, b: int, text: str = None):
        super().__init__(parent)

        self.__lbl_tangent_equation_at_point_bottom = Label(self, 5, 5, 350, 40, r, g, b, text)

        self.setWidget(self.__lbl_tangent_equation_at_point_bottom)

        self.__initUI(x, y, w, h, r, g, b)

    def setText(self, text: str):
        self.__lbl_tangent_equation_at_point_bottom.setText(text)

    def clear(self):
        self.__lbl_tangent_equation_at_point_bottom.clear()

    def __initUI(self, x: int, y: int, w: int, h: int, r: int, g: int, b: int):
        self.setFixedSize(w, h)
        self.move(x, y)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet(
            f"""
                color: rgb({r}, {g}, {b});
                border: 1px solid rgb(0, 0, 0);
                border-radius: 5px;
                font: 12pt;
            """
        )
        self.__lbl_tangent_equation_at_point_bottom.setStyleSheet(
            """
                border-color: rgba(0, 0, 0, 0);
                background-color: rgba(0, 0, 0, 0);
            """
        )
