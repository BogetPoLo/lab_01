class CalculatorError(Exception):
    """Родительский класс для всех ошибок калькулятора"""
    pass


class CalculatorSyntaxError(CalculatorError):
    """Ошибка, если знаки перед или после цифр(по краям) или знаки идут подряд"""
    pass


class CalculatorParenthesisError(CalculatorError):
    """Ошибка, если скобки не корректно расположены"""
    pass


class CalculatorSymbolError(CalculatorError):
    """Ошибка, если есть не допустимый символ"""
    pass


class CalculatorDivisionError(CalculatorError):
    """Ошибка, если деление на 0"""
    def __init__(self, mess = "Ошибка: делить на ноль нельзя."):
        super().__init__(mess)


class ConverterError(Exception):
    """Родительский класс для всех ошибок конвертера"""
    pass


class ConverterAbsZero(ConverterError):
    """Ошибка, если температура ниже абсолютного нуля"""
    pass


class ConverterUncorrectedMeasurements(ConverterError):
    """Ошибка, если разные единицы измерения"""
    def __init__(self, mess = "Ошибка: указаны не корректные единицы измерения."):
        super().__init__(mess)


class RandomError(Exception):
    """Родительский класс для вывода случайной ошибка"""
    def __init__(self, mess = "Ошибка: программа остановилась с неизвестной ошибкой."):
        super().__init__(mess)
