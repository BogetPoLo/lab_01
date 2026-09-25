from collections.abc import Callable
from . import errors

# import errors


def determination_of_the_sign(num_one, num_two, sign_num) -> str:
    """Определяет какой знак у выражения и
    отправляет в функцию для вычисления
    Args: num_one - первое число
          num_two - второе число
          sign_num - знак
    Returns: result - строка с посчитанным выражением типа строка"""
    all_func: dict[str, Callable[[float, float], str]] = {
                "*": multiplication,
                "//": division_without_a_remainder,
                "/": division_with_remainder,
                "%": remainder_of_division,
                "+": addition,
                "-": subtraction
    }
    result: str = ""
    for sign in all_func:
        if sign in sign_num:
            result = all_func[sign](float(num_one), float(num_two))
            break
    return result


def addition(num_one: float, num_two: float) -> str:
    """Сложение двух чисел
        Args: num_one - первое число
              num_two - второе число
        Returns: посчитанное число типа строка"""
    return str(num_one + num_two)


def subtraction(num_one: float, num_two: float) -> str:
    """Вычитание двух чисел
        Args: num_one - первое число
              num_two - второе число
        Returns: посчитанное число типа строка"""
    return str(num_one - num_two)


def multiplication(num_one: float, num_two: float) -> str:
    """Умножение двух чисел
        Args: num_one - первое число
              num_two - второе число
        Returns: посчитанное число типа строка"""
    return str(num_one * num_two)


def division_with_remainder(num_one: float, num_two: float) -> str:
    """Деление двух чисел с остатком
        Args: num_one - первое число
              num_two - второе число
        Returns: посчитанное число типа строка"""
    if num_two == 0:
        raise errors.CalculatorDivisionError()
    return str(num_one / num_two)


def division_without_a_remainder(num_one: float, num_two: float) -> str:
    """Деление двух чисел без остатка
        Args: num_one - первое число
              num_two - второе число
        Returns: посчитанное число типа строка"""
    if num_two == 0:
        raise errors.CalculatorDivisionError()
    return str(num_one // num_two)


def remainder_of_division(num_one: float, num_two: float) -> str:
    """Остаток деления двух чисел
        Args: num_one - первое число
              num_two - второе число
        Return: посчитанное число типа строка"""
    if num_two == 0:
        raise errors.CalculatorDivisionError()
    return str(num_one % num_two)
