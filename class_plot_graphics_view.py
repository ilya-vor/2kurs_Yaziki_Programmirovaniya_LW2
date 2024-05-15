from PyQt6.QtGui import QColor
from pyqtgraph import PlotWidget
import pyqtgraph as pg


class PlotGraphicsView(PlotWidget):
    def __init__(self, parent, x: int, y: int, w: int, h: int):
        super().__init__(parent)
        if w < 0 or h < 0:
            raise Exception(f"[ERROR] Недопустимый размер")

        self.__initUI(x, y, w, h)

    def plot(self, x_coords, y_coords, r: int, g: int, b: int, w: int):
        if r > 255 or g > 255 or b > 255:
            raise Exception(f"[ERROR] Превышен допустимый диапазон для цвета")

        if w < 0:
            raise Exception(f"[ERROR] Недопустимый размер")

        pen = pg.mkPen(color=QColor(r, g, b), width=w)
        self.plotItem.plot(x_coords, y_coords, pen=pen)

    def __initUI(self, x: int, y: int, w: int, h: int):
        self.setBackground(QColor(255, 255, 255))
        self.setGeometry(x, y, w, h)
        self.showGrid(x=True, y=True, alpha=1)
