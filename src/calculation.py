from collections.abc import Callable


def determination_of_the_sign(nums: str) -> str | None:
    """Определяет какой знак у выражения и
    отправляет в функцию для вычисления
    Args: nums - выражение со знаком. Примеры: 1+2, 2/3"""
    all_func: dict[str, Callable[[list[int]], str]] = {
                "+": addition,
                "-": subtraction,
                "*": multiplication,
                "/": integer_division
    }

    for sing in all_func:
        if sing in nums:
            list_n: list[int] = list(map(int, nums.split(sing)))
            return all_func[sing](list_n)
    return None


def addition(list_n: list[int]) -> str:
    """Сложение двух чисел
        Args: list_n - список с двумя числами
        Returns: посчитанное число типа строка"""
    return str(list_n[0] + list_n[-1])


def subtraction(list_n: list[int]) -> str:
    """Вычитание двух чисел
        Args: list_n - список с двумя числами
        Returns: посчитанное число типа строка"""
    return str(list_n[0] - list_n[-1])


def multiplication(list_n: list[int]) -> str:
    """Умножение двух чисел
        Args: list_n - список с двумя числами
        Returns: посчитанное число типа строка"""
    return str(list_n[0] * list_n[-1])


def integer_division(list_n: list[int]) -> str:
    """Деление двух чисел
        Args: list_n - список с двумя числами
        Returns: посчитанное число типа строка"""
    return str(list_n[0] / list_n[-1])
