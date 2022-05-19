import math
from numpy import arange

FILE_IN = "C:/Users/Dasxunya/Desktop/ITMO/comp_math/lab_3/input.txt"


def console_input():
    global a, b
    while True:
        try:
            print("Введите пределы интегрирования [a; b], где a < b:")
            a = float(input("a ~ "))
            b = float(input("b ~ "))
            if a > b:
                print("Требуется a < b, значения границ были переставлены местами")
                temp = a
                a = b
                b = temp
            elif a == b:
                print("Уточнение: Требуется  a < b")
                raise ValueError
            break
        except (ValueError, TypeError):
            print("Проверьте формат введенных данных (разделять точкой)")

    while True:
        try:
            error = float(input("Погрешность вычисления ∈ (0; 1): "))
            if error <= 0 or error >= 1:
                raise ArithmeticError
            break
        except (ValueError, ArithmeticError):
            print("Погрешность вычисления должна быть положительным числом.")

    return a, b, error


def console_decide():
    global function_data, d_func, abs_error, n, answer, number
    try:
        print('Выберите функцию:\n1 ~ x⁴ + 4\n2 ~ 1/x\n3 ~ sin(x)/x\n4 ~ 1/sin(x)')
        number = int(input("> "))
        function_data, d_func = getfunc(number)
        d = checkfunc(number)
    except (ValueError, TypeError, ArithmeticError):
        print("Введите команду, предложенную в меню!")
        exit(-1)
    a, b, error = console_input()
    if number == 3:
        answer, abs_error, n = first_kind(function_data, a, b, d_func, error, d)
        print(
            f"\nРезультат по методу Симпсона: {answer:.8f}\nАбсолютная погрешность: {abs_error}\nКоличество разбиений: {n}")
        exit(0)
    try:
        answer, abs_error, n = simpson_method(function_data, a, b, d_func, error)
        return answer, abs_error, n
    except ArithmeticError:
        print("Будьте внимательны! неустранимый разрыв 2-го рода не должен попадать в промежуток")
        exit(-1)
    except ValueError:
        print("Проверьте ОДЗ функции и попробуйте снова!")
        exit(-1)


def getfunc(number):
    if number == 1:
        func = lambda x: x ** 4 + 4
        d_func = lambda x: 24 + 0 * x
        return func, d_func
    if number == 2:
        func = lambda x: 1 / x
        d_func = lambda x: 24 * math.pow(x, -5)
        return func, d_func
    if number == 3:
        func = lambda x: math.sin(x) / x
        d_func = lambda x: x * math.pow(x, -4) * (
                4 * x * math.cos(x) - 12 * math.sin(x) + 24 * math.sin(x) * math.pow(x, -2) - 24 * math.cos(
            x) * math.pow(x, -1) + math.sin(x) * math.pow(x, 2))
        return func, d_func
    if number == 4:
        func = lambda x: 1 / math.sin(x)
        d_func = lambda x: (5 + (28 * math.cos(x) ** 2) / (math.sin(x) ** 2) + (24 * math.cos(x) ** 4) / (
                math.sin(x) ** 4)) / math.sin(x)
        return func, d_func
    else:
        return None


def checkfunc(number):
    global d
    if number == 1:
        print("Выбрана обычная функция")
        d = 0
    if number == 2:
        print("Выбрана функция с неустранимым разрывом в точке 0")
        d = 0
    if number == 3:
        print(
            "Выбрана функция с точкой устранимого разрыва 1-го рода!\nКаким образом устранить?\n1 ~ суммой интегралов\n2 ~ средним алгоритмическим точек")
        d = int(input())
        if d == 1:
            print("Разрыв устранен суммой интегралов")
        if d == 2:
            print("Разрыв устранен средним алгоритмическим точек")
    if number == 4:
        print("Выбрана функция с опасным ОДЗ")
        d = 0
    return d


def simpson_method(f, left, right, d_func, error):
    """ Метод Симпсона """
    global answer, abs_error
    n = 1
    res = 1
    prev_res = 0
    while math.fabs(res - prev_res) > error:
        n *= 2
        prev_res = res
        h = (right - left) / n
        s1 = 0
        s2 = 0
        fourth_derivatives = [0 for j in range(n + 1)]
        for i in range(n + 1):
            if i % 2 == 0:
                try:
                    s1 = s1 + f(left + i * h)
                except ZeroDivisionError:
                    print("Значение границы было изменено, т.к находится вне ОДЗ")
                    left = left + 1e-12
                    right = right - 1e-12
            else:
                s2 = s2 + f(left + i * h)
            # подсчет четвертой производной точек
            fourth_derivatives[i] = d_func(left + i * h)
        r = get_r(left, right, n, d_func)
        answer = h / 3 * (f(left) + f(right) + 2 * s1 + 4 * s2)
        res = answer
        abs_error = -(1 / 90) * h ** 5 * f(res - prev_res) ** 4
        if r > math.fabs(answer):
            raise ArithmeticError
    return answer, abs_error, n


def get_r(a, b, n, d_func):
    r = 0
    for i in arange(a, b, ((b - a) / 1000)):
        try:
            cur_r = d_func(i)
            cur_r *= math.pow((b - a), 5)
            cur_r /= (2880 * math.pow(n, 4))
        except ValueError:
            cur_r = 0
        if abs(cur_r) > r:
            r = abs(cur_r)
    return r


def first_kind(function_data, a, b, d_func, error, d):
    global abs_error1, abs_error2, n1, n2, res2, res1
    left1 = a
    right1 = 0 - error
    left2 = 0 + error
    right2 = b
    if d == 1:
        res1, abs_error1, n1 = simpson_method(function_data, left1, right1, d_func, error)
        res2, abs_error2, n2 = simpson_method(function_data, left2, right2, d_func, error)
        return res1 + res2, abs_error1 + abs_error2, n1 + n2
    if d == 2:
        res, abs_error, n = simpson_method(function_data, left1, right2, d_func, error)
        return res, abs_error, n

