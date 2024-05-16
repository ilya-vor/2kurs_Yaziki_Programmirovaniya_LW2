import math
import numpy as np


class Calculator:
    def __init__(self, start_x: int, end_x: int, amount_of_points: int):
        if start_x >= end_x:
            raise Exception('[ERROR] Неверно задан диапазон')

        if amount_of_points <= 0:
            raise Exception('[ERROR] Неверно задано количество точек')

        self.__bin_operators = ['^', '*', '/', '+', '-']
        self.__un_operators = ['~', 'cos', 'sin','ln']
        self.__operators = self.__bin_operators + self.__un_operators

        self.__range = (start_x, end_x)

        self.__x_coords = np.linspace(start_x, end_x, amount_of_points)
        self.__y_coords_expression_rpn = []
        self.__y_coords_derivative_of_an_expression_rpn = []
        self.__y_coords_tangent_equation_rpn = []

        self.__expression_in = ""
        self.__expression_rpn = ""
        self.__derivative_of_an_expression_rpn = ""
        self.__derivative_of_an_expression_in = ""
        self.__tangent_equation_with_parameter_rpn = ""
        self.__tangent_equation_rpn = ""
        self.__tangent_equation_in = ""

    def calc(self, expression_in: str):
        if expression_in.count('(') != expression_in.count(')'):
            raise Exception('[ERROR] Неверная формула')

        self.__expression_rpn = self.__convert_to_rpn(expression_in)
        self.__expression_in = expression_in

        self.__compute_expression()

        self.__derivative_of_an_expression_rpn = self.__diff(self.__expression_rpn)

        self.__compute_derivative()

        self.__derivative_of_an_expression_in = self.__convert_to_in(self.__derivative_of_an_expression_rpn)

        self.__generate_tangent_equation_with_parameter_rpn()

    def calc_tangent(self, parameter_a: float):
        if not self.__tangent_equation_with_parameter_rpn:
            return -1

        self.__generate_tangent_equation_rpn(parameter_a)
        self.__compute_tangent()
        self.__tangent_equation_in = self.__convert_to_in(self.__tangent_equation_rpn)

    def get_range(self):
        return self.__range

    def get_derivative_of_an_expression_in(self):
        return self.__derivative_of_an_expression_in

    def get_tangent_equation_in(self):
        return self.__tangent_equation_in

    def get_y_coords_tangent_equation_rpn(self):
        return self.__y_coords_tangent_equation_rpn

    def get_y_coords_expression_rpn(self):
        return self.__y_coords_expression_rpn

    def get_y_coords_derivative_of_an_expression_rpn(self):
        return self.__y_coords_derivative_of_an_expression_rpn

    def get_x_coords(self):
        return self.__x_coords

    def __compute_tangent(self):
        y_coords_tangent_equation_rpn_list = []
        for x in self.__x_coords:
            y_coords_tangent_equation_rpn_list.append(self.__compute(self.__tangent_equation_rpn, x))
        self.__y_coords_tangent_equation_rpn = np.array([y for y in y_coords_tangent_equation_rpn_list], dtype=float)

    def __compute_derivative(self):
        y_coords_derivative_of_an_expression_rpn_list = []
        for x in self.__x_coords:
            y_coords_derivative_of_an_expression_rpn_list.append(
                self.__compute(self.__derivative_of_an_expression_rpn, x))
        self.__y_coords_derivative_of_an_expression_rpn = np.array(
            [y for y in y_coords_derivative_of_an_expression_rpn_list],
            dtype=float)

    def __compute_expression(self):
        y_coords_expression_in_rpn_list = []
        for x in self.__x_coords:
            y_coords_expression_in_rpn_list.append(self.__compute(self.__expression_rpn, x))
        self.__y_coords_expression_rpn = np.array([y for y in y_coords_expression_in_rpn_list], dtype=float)

    def __generate_tangent_equation_rpn(self, parameter_a: float):
        if parameter_a >= 0:
            self.__tangent_equation_rpn = self.__tangent_equation_with_parameter_rpn.replace('a', str(parameter_a))
        else:
            self.__tangent_equation_rpn = self.__tangent_equation_with_parameter_rpn.replace('a',
                                                                                             f"{parameter_a * (-1)} ~")

    def __generate_tangent_equation_with_parameter_rpn(self):
        f_a = self.__expression_rpn.replace('x', 'a')
        df_a = self.__derivative_of_an_expression_rpn.replace('x', 'a')
        self.__tangent_equation_with_parameter_rpn = f"{f_a} {df_a} x a - * +"

    def __compute(self, expression_rpn: str, x: float = None):
        expr = expression_rpn.split()
        stack = []
        for elem in expr:
            if elem == 'x':
                if not x and x != 0.0:
                    raise Exception("[ERROR] Отсутствует значение для параметра x")
                operand = float(x)
                stack.append(operand)
                continue

            try:
                operand = float(elem)
                stack.append(operand)
                continue
            except ValueError:
                if not (elem in self.__operators):
                    raise Exception('[ERROR] Неверная формула')

            try:
                operand_2 = stack.pop()
            except Exception:
                raise Exception('[ERROR] Неверная формула')

            match elem:
                case "~":
                    stack.append(operand_2 * (-1))
                    continue
                case "sin":
                    stack.append(math.sin(operand_2))
                    continue
                case "cos":
                    stack.append(math.cos(operand_2))
                    continue
                case "ln":
                    stack.append(math.log(operand_2,2.718))
                    continue

            try:
                operand_1 = stack.pop()
            except Exception:
                raise Exception('[ERROR] Неверная формула')

            match elem:
                case "^":
                    base = operand_1
                    exponent = operand_2
                    stack.append(base ** exponent)
                case "+":
                    stack.append(operand_1 + operand_2)
                case "-":
                    stack.append(operand_1 - operand_2)
                case "*":
                    stack.append(operand_1 * operand_2)
                case "/":
                    try:
                        stack.append(operand_1 / operand_2)
                    except ZeroDivisionError:
                        raise ZeroDivisionError('[ERROR] Попытка деления на нуль')

        if len(stack) != 1:
            raise Exception('[ERROR] Неверная формула')

        return stack[0]

    def __get_operator_priority(self, operator: str):
        match operator:
            case 'cos':
                return 6
            case 'sin':
                return 6
            case '~':
                return 5
            case '^':
                return 4
            case '*':
                return 3
            case '/':
                return 3
            case '+':
                return 2
            case '-':
                return 2
            case '(':
                return 1

    def __convert_to_rpn(self, expression_in: str):
        expression_rpn = ""
        operator_stack = []

        i = 0
        while i < len(expression_in):
            elem = expression_in[i]

            if elem == 'e':
                expression_rpn += '2.71828'
                i += 1
                continue

            if elem.isdigit() or elem == '.' or elem == ' ' or elem == 'x':
                expression_rpn += elem
                i += 1
                continue

            if elem == '(':
                expression_rpn += ' '
                operator_stack.append(elem)
                i += 1
                continue

            if elem == ')':
                try:
                    while len(operator_stack) > 0 and operator_stack[-1] != '(':
                        expression_rpn += ' '
                        expression_rpn += operator_stack.pop()
                    expression_rpn += ' '
                    operator_stack.pop()
                    i += 1
                    continue
                except Exception:
                    raise Exception('[ERROR] Неверная формула')

            if elem == '-' and (i == 0 or i >= 1 and expression_in[i - 1] == '('):
                elem = '~'

            try:
                if (elem == 'p'
                        and
                        expression_in[i + 1] == 'i'):
                    expression_rpn += '3.14159'
                    i += 2
                    continue

                if (elem == 's'
                        and
                        expression_in[i + 1] == 'i'
                        and
                        expression_in[i + 2] == 'n'
                        and
                        expression_in[i + 3] == '('):
                    elem = 'sin'
                    i += 2

                if (elem == 'c'
                        and
                        expression_in[i + 1] == 'o'
                        and
                        expression_in[i + 2] == 's'
                        and
                        expression_in[i + 3] == '('):
                    elem = 'cos'
                    i += 2
            except IndexError:
                raise Exception('[ERROR] Неверная формула')

            if elem in self.__operators:
                if len(operator_stack) > 0 and elem == '^' and operator_stack[-1] == '^':
                    pass
                else:
                    while (len(operator_stack) > 0
                           and
                           self.__get_operator_priority(operator_stack[-1]) >= self.__get_operator_priority(elem)):
                        expression_rpn += ' '
                        expression_rpn += operator_stack.pop()

                expression_rpn += ' '
                operator_stack.append(elem)
                i += 1
            else:
                raise Exception('[ERROR] Неверная формула')

        for i in range(len(operator_stack) - 1, -1, -1):
            expression_rpn += ' '
            expression_rpn += operator_stack[i]

        flag = False
        normalized_expression_rpn = ""

        for elem in expression_rpn:
            if elem == ' ':
                if flag:
                    flag = False
                    normalized_expression_rpn += elem
            else:
                flag = True
                normalized_expression_rpn += elem

        return normalized_expression_rpn

    def __diff_mul(self, operand_1: str, operand_2: str):
        expr = f"{self.__diff(operand_1)} {operand_2} * {operand_1} {self.__diff(operand_2)} * +"

        return expr

    def __diff_div(self, operand_1: str, operand_2: str):
        expr = f"{self.__diff(operand_1)} {operand_2} * {operand_1} {self.__diff(operand_2)} * - {operand_2} 2 ^ /"

        return expr

    def __diff_add(self, operand_1: str, operand_2: str):
        expr = f"{self.__diff(operand_1)} {self.__diff(operand_2)} +"

        return expr

    def __diff_sub(self, operand_1: str, operand_2: str):
        expr = f"{self.__diff(operand_1)} {self.__diff(operand_2)} -"

        return expr

    def __diff_pow(self, operand_1: str, operand_2: str):
        if 'x' in operand_2:
            if 'x' in operand_1:
                expr = f"{operand_1} {operand_2} ^ {operand_1} ln * {self.__diff(operand_2)} * {operand_1} {operand_2} ^ {self.__diff(operand_2)} * +"
            else:
                expr = f"{operand_1} {operand_2} ^ {math.log(float(operand_1), math.e)} * {self.__diff(operand_2)} *"
        else:
            expr = f"{operand_2} {operand_1} {operand_2} 1 - ^ * {self.__diff(operand_1)} *"

        return expr

    def __diff_un_min(self, operand_1: str):
        expr = f"{self.__diff(operand_1)} ~"

        return expr

    def __diff_sin(self, operand_1: str):
        expr = f"{operand_1} cos {self.__diff(operand_1)} *"

        return expr

    def __diff_cos(self, operand_1: str):
        expr = f"{operand_1} sin ~ {self.__diff(operand_1)} *"

        return expr

    def __get_operands(self, subexpression_rpn: list):
        operand_stack = []

        for i in range(len(subexpression_rpn)):
            elem = subexpression_rpn[i]

            if not (elem in self.__bin_operators) and not (elem in self.__un_operators):
                operand_stack.append(elem)
                continue

            if elem in self.__bin_operators:
                operand_2 = [operand_stack.pop()]
                operand_1 = [operand_stack.pop()]
                operator = [elem]
                operand = ' '.join([operand_1[0], operand_2[0], operator[0]])
                operand_stack.append(operand)
                continue

            if elem in self.__un_operators:
                operand_1 = [operand_stack.pop()]
                operator = [elem]
                operand = ' '.join([operand_1[0], operator[0]])
                operand_stack.append(operand)
                continue

        return operand_stack

    def __diff(self, expression_rpn: str):
        """
        if expression_rpn == "x x ^":
        return "x x ^ x ln * x x ^ +"
        """


        expr = expression_rpn.split()
        derivative_of_an_expression_rpn = ""
        elem = expr[-1]

        try:
            float(elem)
            elem = 'number'
        except ValueError:
            pass

        match elem:
            case 'number':
                derivative_of_an_expression_rpn = '0'
                return derivative_of_an_expression_rpn
            case 'x':
                derivative_of_an_expression_rpn = '1'
                return derivative_of_an_expression_rpn

        if elem in self.__bin_operators:
            operands = self.__get_operands(expr[0:-1])
            operand_1 = operands[0]
            operand_2 = operands[1]
            match elem:
                case '*':
                    derivative_of_an_expression_rpn = self.__diff_mul(operand_1, operand_2)
                case '/':
                    derivative_of_an_expression_rpn = self.__diff_div(operand_1, operand_2)
                case '+':
                    derivative_of_an_expression_rpn = self.__diff_add(operand_1, operand_2)
                case '-':
                    derivative_of_an_expression_rpn = self.__diff_sub(operand_1, operand_2)
                case '^':
                    derivative_of_an_expression_rpn = self.__diff_pow(operand_1, operand_2)

            return derivative_of_an_expression_rpn

        if elem in self.__un_operators:
            operands = self.__get_operands(expr[0:-1])
            operand_1 = operands[0]
            match elem:
                case '~':
                    derivative_of_an_expression_rpn = self.__diff_un_min(operand_1)
                case 'sin':
                    derivative_of_an_expression_rpn = self.__diff_sin(operand_1)
                case 'cos':
                    derivative_of_an_expression_rpn = self.__diff_cos(operand_1)
            return derivative_of_an_expression_rpn

    def __convert_to_in(self, expression_rpn: str):
        expr = expression_rpn.split()
        stack = []

        for elem in expr:
            if elem == 'x':
                stack.append(elem)
                continue

            try:
                elem = str(round(float(elem),5))
                stack.append(elem)
                continue
            except ValueError:
                pass

            if elem in self.__bin_operators:
                operand_2 = stack.pop()
                operand_1 = stack.pop()
                operator = elem

                try:
                    float(operand_2)
                    float(operand_1)

                    operand = str(self.__compute(f"{operand_1} {operand_2} {operator}"))
                    if operand == '0.0' or operand == '-0.0':
                        stack.append('0')
                    else:
                        stack.append(str(round(float(operand),5)))
                    continue
                except ValueError:
                    pass

                try:
                    number_2 = round(float(operand_2),5)
                    match operator:
                        case '+', '-':
                            if number_2 == 0.0 or number_2 == -0.0:
                                operand = operand_1
                                stack.append(operand)
                                continue
                        case '*':
                            if number_2 == 0.0 or number_2 == -0.0:
                                operand = "0"
                                stack.append(operand)
                                continue
                            elif number_2 == 1.0:
                                operand = operand_1
                                stack.append(operand)
                                continue
                            elif number_2 == -1.0:
                                operand = -operand_1
                                stack.append(operand)
                                continue
                        case '/':
                            if number_2 == 0.0 or number_2 == -0.0:
                                raise ZeroDivisionError('[ERROR] Попытка деления на нуль')
                            elif number_2 == 1.0:
                                operand = operand_1
                                stack.append(operand)
                                continue
                            elif number_2 == -1.0:
                                operand = -operand_1
                                stack.append(operand)
                                continue
                        case '^':
                            if number_2 == 0.0 or number_2 == -0.0:
                                operand = "1"
                                stack.append(operand)
                                continue
                            elif number_2 == 1.0:
                                operand = operand_1
                                stack.append(operand)
                                continue
                except ValueError:
                    pass

                try:
                    number_1 = round(float(operand_1),5)
                    match operator:
                        case '+':
                            if number_1 == 0.0 or number_1 == -0.0:
                                operand = operand_2
                                stack.append(operand)
                                continue
                        case '-':
                            if number_1 == 0.0 or number_1 == -0.0:
                                operand = operand_2
                                stack.append(operand)
                                continue
                        case '*':
                            if number_1 == 0.0 or number_1 == -0.0:
                                operand = "0"
                                stack.append(operand)
                                continue
                            elif number_1 == 1.0:
                                operand = operand_2
                                stack.append(operand)
                                continue
                            elif number_1 == -1.0:
                                operand = f"-{operand_2}"
                                stack.append(operand)
                                continue
                        case '/':
                            if number_1 == 0.0 or number_1 == -0.0:
                                operand = "0"
                                stack.append(operand)
                        case '^':
                            if number_1 == 1.0:
                                operand = "1"
                                stack.append(operand)
                                continue
                except ValueError:
                    pass

                operand = f"({operand_1} {operator} {operand_2})"
                stack.append(operand)
                continue

            if elem in self.__un_operators:
                operand_1 = stack.pop()
                operator = elem

                try:
                    float(operand_1)
                    operand = str(self.__compute(f"{operand_1} {operator}"))
                    if operand == '0.0' or operand == '-0.0':
                        stack.append('0')
                    else:
                        stack.append(str(round(float(operand),5)))
                    continue
                except ValueError:
                    pass

                if elem == '~':
                    operator = '-'
                    operand = f"({operator}({operand_1}))"
                else:
                    operator = elem
                    operand = f"({operator}({operand_1}))"
                stack.append(operand)
                continue
        if '(' in stack and ')' in stack and stack[0][0] == '(' and stack[0][-1] == ')':
            expr_in = stack[0][1:-1]
        else:
            expr_in = stack[0]

        return expr_in
