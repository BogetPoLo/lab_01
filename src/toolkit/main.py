import argparse
import sys

from .converter import convert_units
from .errors import CalculatorError, ConverterError
from .tokenization import tokenization


def calculator(expression: str) -> None:
    """точка входа для вычисления"""
    result: str = tokenization(expression)
    sys.stdout.write(f"{result}\n")


def converter(value: float, from_unit: str, to_unit: str) -> None:
    """точка входа для конвертации"""
    result: float = convert_units(value, from_unit, to_unit)
    sys.stdout.write(f"{result}\n")


def main() -> None:
    """точка входа"""
    parser = argparse.ArgumentParser(
        description="Консольная утилита: калькулятор и конвертер",
        prog="toolkit"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        help="Команды"
    )

    """подкоманда calc: python -m toolkit calc 'expression' """
    parser_calc = subparsers.add_parser(
        "calc",
        help="Вычисление математических выражений с использованием знаков: *, /, //, %%, +, -"
    )
    parser_calc.add_argument(
        "expression",
        type=str,
        help="Математическое выражение"
    )

    """подкоманда convert: python -m toolkit convert value --from unit --to unit """
    parser_convert = subparsers.add_parser(
        "convert",
        help="Конвертов величин (длина: mm, cm, m, km; масса: g, kg; температура: c, f, k"
    )

    parser_convert.add_argument(
        "value",
        type=float,
        help="Значение для конвертации"
    )

    parser_convert.add_argument(
        "--from",
        required=True,
        dest="from_unit",
        help="Исходная единица измерения"
    )

    parser_convert.add_argument(
        "--to",
        required=True,
        dest="to_unit",
        help="Итоговая единица измерения"
    )

    args = parser.parse_args()

    try:
        if args.command == "calc":
            calculator(args.expression)
        elif args.command == "convert":
            converter(args.value, args.from_unit, args.to_unit)
    except (CalculatorError, ConverterError) as err:
        sys.stderr.write(f"{err}\n")
        sys.exit(2)



if __name__ == "__main__":
    main()
