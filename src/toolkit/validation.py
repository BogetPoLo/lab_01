from . import errors
from . import constants

# import errors
# import constants


def checking_the_signs_at_the_edges(signs: tuple[str, ...]) -> bool:
    """Проверяют есть ли знаки по краям
    Args: signs - знак
    Returns: True - по краям знаков или нет(если спереди есть, то значит он корректен, только для +/-)
             Исключение - знак записан не правильно"""
    for sign in signs:
        for operation in constants.FIRST_PRIORITY_OPERATIONS:
            if operation not in sign:
                continue
            raise errors.CalculatorSyntaxError(
                f"Ошибка: перед первым или после последнего числа не может быть знака {sign}."
            )
    if any([True if sign in signs[-1] else False for sign in constants.SECOND_PRIORITY_OPERATIONS]):
        raise errors.CalculatorSyntaxError("Ошибка: после последнего числа не может быть знака -/+.")
    return True


def validation_of_input_characters(expression: str) -> bool:
    """Проверяет есть ли лишние знаки
    Args: expression - все выражение
    Returns: True - все корректно
             исключение - есть лишние знаки"""
    for exp in expression:
        for symbol in exp:
            if (symbol not in constants.ALL_OPERATIONS and
                    symbol not in constants.ALL_NUM and
                    symbol not in constants.OPEN_PARENTHESIS and
                    symbol not in constants.CLOSE_PARENTHESIS and
                    symbol not in " "):
                raise errors.CalculatorSymbolError(f"Ошибка: не совместимый символ {symbol}.")
    return True


def check_sign(signs: str) -> bool:
    """Проверяет корректно ли записаны знаки
        Args: signs - знак(и)
        Returns: True - знак записан корректно
                 исключение - знак записан не корректно"""

    all_sign: dict[str, bool] = {
        "-": False,
        "+": False,
        "*": False,
        "/": False,
        "//": False,
        "%": False
    }

    for s in signs:
        all_sign[s] = True
        if (s in constants.FIRST_PRIORITY_OPERATIONS and
                any([all_sign[i] for i in constants.SECOND_PRIORITY_OPERATIONS])):
            # Если встретился знак второго порядка, но до этого были первого порядка, то выпадает ошибка
            raise errors.CalculatorSyntaxError("Ошибка: не корректная запись знака.")
    if len([1 for i in constants.FIRST_PRIORITY_OPERATIONS if all_sign[i]]) > 1:
        # Если встретилось несколько знаков первого порядка, то выпадает ошибка
        raise errors.CalculatorSyntaxError("Ошибка: не корректная запись знака.")
    return True


def validate_temperature(value: float, unit: str) -> bool:
    """Определяет температура ниже абсолютного нуля или нет
    Args: value - значение
          unit - единица измерения
    Returns: True - выше абсолютного нуля
             исключение - ниже абсолютного нуля"""
    if value < constants.ABS_ZERO[unit]:
        raise errors.ConverterAbsZero("Ошибка: ниже абсолютного нуля.")
    return True
