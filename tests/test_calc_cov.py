import pytest  # type: ignore

from toolkit import errors
from toolkit.converter import convert_units
from toolkit.tokenization import tokenization

"""положительные тесты"""


def test_positive_simple_math():
    """простые вычисления"""
    assert float(tokenization("2 + 2 * 2")) == 6.0


def test_positive_parentheses_and_priority():
    """проверка скобок"""
    assert float(tokenization("12.5 - (2.5 * 1.0 - 3.5)")) == 13.5


def test_positive_unar_minus():
    """обработка унарного минуса"""
    assert float(tokenization("-5 + 10")) == 5.0


def test_positive_int_and_float_division():
    """деление с остатком"""
    assert float(tokenization("10 // 3 + 10 % 3")) == 4.0


def test_positive_convert_len():
    """конвертация длин"""
    assert convert_units(1.5, "km", "m") == 1500.0


def test_positive_convert_mass():
    """конвертация масс"""
    assert convert_units(2500, "g", "kg") == 2.5


def test_positive_convert_temp():
    """конвертация темп"""
    assert convert_units(0, "c", "f") == 32.0


def test_positive_convert_temp_two():
    """конвертация темп"""
    assert convert_units(273.15, "k", "c") == 0.0


"""отрицательные тесты"""


def test_negative_division_by_zero():
    """деление на ноль"""
    with pytest.raises(errors.CalculatorDivisionError):
        tokenization("10/0")


def test_negative_invalid_parenthesis():
    """скобки не цельные"""
    with pytest.raises(errors.CalculatorParenthesisError):
        tokenization("12 - (2 * 1 - 3")


def test_negative_invalid_operator_at_edge():
    """знак второго порядка в конце"""
    with pytest.raises(errors.CalculatorSyntaxError):
        tokenization("5 + 3 - ")


def test_negative_invalid_character():
    """случайные символы"""
    with pytest.raises(errors.CalculatorSymbolError):
        tokenization("10 - ee")


def test_negative_temp_abs_zero():
    """темп ниже 0"""
    with pytest.raises(errors.ConverterAbsZero):
        convert_units(-300, "c", "f")


def test_negative_units():
    with pytest.raises(errors.ConverterUncorrectedMeasurements):
        convert_units(10, "m", "g")


def test_negative_empty_expression():
    """пустая строка"""
    with pytest.raises(errors.CalculatorSyntaxError):
        tokenization("")
