from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import QTimer
from class_plot_graphics_view import PlotGraphicsView
from class_button import Button
from class_expression_line_edit import ExpressionLineEdit
from class_label import Label
from class_scroll_label import ScrollLabel
import calculator as clc


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.__graph = PlotGraphicsView(self, 20, 20, 450, 450)

        self.__graph.scene().sigMouseClicked.connect(self.__calcTangent)

        self.__lbl_left_expression_in = Label(self, 490, 20, 50, 50, 34, 139, 34, "y(x)")

        self.__input_expression_line_edit = ExpressionLineEdit(self, 550, 20, 300, 50)

        self.__btn_clear = Button(self, 790, 90, 60, 30, "Clear", slot=self.__clear)

        self.__btn_calc = Button(self, 710, 90, 60, 30, "Calc", slot=self.__calc)

        self.__lbl_left_derivative_of_an_expression_in = Label(self, 490, 140, 50, 50, 0, 0, 205, "y'(x)")

        self.__scroll_label_right_derivative_of_an_expression_in = ScrollLabel(self, 550, 140, 300, 50, 0, 0, 205)

        self.__scroll_label_tangent_equation_at_point_top = ScrollLabel(self, 490, 210, 360, 50, 255, 0, 0,
                                                                        "Для построения касательной \nнажмите по графику")

        self.__scroll_label_tangent_equation_at_point_bottom = ScrollLabel(self, 490, 270, 360, 50, 255, 0, 0)

        self.__calculator = clc.Calculator(1, 20, 100)

        self.__initUI()

    def mousePressEvent(self, a0):
        self.setFocus()

    def __initUI(self):
        self.setWindowTitle("User function graph")
        self.setFixedSize(870, 490)
        self.setStyleSheet(
            """
                background-color: rgb(255, 255, 255);
                color: rgb(0, 0, 0);
                border: 1px solid rgb(0, 0, 0);
            """
        )
        QTimer.singleShot(1, self.__centerWindow)

    def __centerWindow(self):
        app_rectangle = self.frameGeometry()
        screen_rectangle = self.screen().availableGeometry().center()
        app_rectangle.moveCenter(screen_rectangle)
        self.move(app_rectangle.topLeft())

    def __clear(self):
        self.__graph.clear()
        self.__input_expression_line_edit.clear()
        self.__scroll_label_right_derivative_of_an_expression_in.clear()
        self.__scroll_label_tangent_equation_at_point_top.setText("Для построения касательной \nнажмите по графику")
        self.__scroll_label_tangent_equation_at_point_bottom.clear()

    def __calcTangent(self, evt):
        if not self.__graph.listDataItems():
            return -1

        pos = evt.pos()
        if not self.__graph.sceneBoundingRect().contains(pos):
            return -1

        mouse_point = self.__graph.plotItem.vb.mapToView(pos)
        parameter_a = mouse_point.x()

        start_x, end_x = self.__calculator.get_range()

        if parameter_a < start_x or parameter_a > end_x:
            return -1

        data_items = self.__graph.listDataItems()
        if len(data_items) == 3:
            self.__graph.removeItem(data_items[-1])

        self.__calculator.calc_tangent(parameter_a)

        self.__graph.plot(self.__calculator.get_x_coords(),
                          self.__calculator.get_y_coords_tangent_equation_rpn(),
                          255, 0, 0, 2)

        self.__scroll_label_tangent_equation_at_point_top.setText(f"Уравнение касательной в точке {round(parameter_a,2)}")
        self.__scroll_label_tangent_equation_at_point_bottom.setText(self.__calculator.get_tangent_equation_in())

    def __calc(self):
        expression_in = self.__input_expression_line_edit.finish()
        if not expression_in:
            return -1
        self.__clear()
        self.__input_expression_line_edit.setText(expression_in)
        try:
            self.__calculator.calc(expression_in)

            self.__graph.plot(self.__calculator.get_x_coords(),
                              self.__calculator.get_y_coords_derivative_of_an_expression_rpn(),
                              0, 0, 205, 6)
            self.__graph.plot(self.__calculator.get_x_coords(),
                              self.__calculator.get_y_coords_expression_rpn(),
                              34, 139, 34, 10)

            self.__scroll_label_right_derivative_of_an_expression_in.setText(
                self.__calculator.get_derivative_of_an_expression_in())

            self.__input_expression_line_edit.success()

        except Exception as e:
            print(e)
            self.__input_expression_line_edit.error()
