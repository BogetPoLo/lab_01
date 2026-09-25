import json

from . import constants
from . import validation
from . import errors

# import constants
# import validation
# import errors


def write_json(start_expression: str, result_expression: str, from_unit: str, to_unit: str) -> None:
    data: dict[str, str] = {
        "start": start_expression,
        "result": result_expression,
        "from": from_unit,
        "to": to_unit
    }

    with open("config.json", mode="w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def convert_units(value: float, from_unit: str, to_unit: str) -> float:
    """Входная функция для конвертации
    Args: value - значение
          from_unit - исходная единица измерения
          to_unit - итоговая единица измерения
    Returns: результат"""
    f_unit = from_unit.strip().lower()
    t_unit = to_unit.strip().lower()

    res: float = -9999

    # для счета длины
    if f_unit in constants.LENGTH and t_unit in constants.LENGTH:
        res = convert_length(value, f_unit, t_unit)

    # для счета масс
    if f_unit in constants.MASS and t_unit in constants.MASS:
        res = convert_mass(value, f_unit, t_unit)

    # для счета температуры
    if f_unit in constants.ABS_ZERO and t_unit in constants.ABS_ZERO:
        validation.validate_temperature(value, f_unit)
        res = convert_abs_zero(value, f_unit, t_unit)

    if res != -9999:
        write_json(str(value), str(res), from_unit, to_unit)
        return res

    raise errors.ConverterUncorrectedMeasurements()


def convert_length(value: float, f_unit: str, t_unit: str) -> float:
    """конвертирует длину
    Args: value - значение
          from_unit - исходная единица измерения
          to_unit - итоговая единица измерения
    Returns: результат"""
    base_value: float = value * constants.LENGTH[f_unit]
    return float(base_value / constants.LENGTH[t_unit])

def convert_mass(value: float, f_unit: str, t_unit: str) -> float:
    """конвертирует массу
    Args: value - значение
          from_unit - исходная единица измерения
          to_unit - итоговая единица измерения
    Returns: результат"""
    base_value: float = value * constants.MASS[f_unit]
    return float(base_value / constants.MASS[t_unit])


def convert_abs_zero(value: float, f_unit: str, t_unit: str) -> float:
    """конвертирует температуру
    Args: value - значение
          from_unit - исходная единица измерения
          to_unit - итоговая единица измерения
    Returns: результат"""
    celsius: float = 0.0
    if f_unit == "c":
        celsius = value
    elif f_unit == "f":
        celsius = (value - 32) * 5 / 9
    else:
        celsius = value - 273.15

    result: float = 0.0
    if t_unit == "c":
        result = celsius
    elif t_unit == "f":
        result = celsius * 9 / 5 + 32
    else:
        result = celsius + 273.15

    validation.validate_temperature(result, t_unit)
    return float(result)
