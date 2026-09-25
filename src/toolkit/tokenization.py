from re import findall
import json

from . import constants
from . import errors
from . import validation
from . import calculation

# import constants
# import errors
# import validation
# import calculation


def collapse_unar_signs(sign_chain: str) -> str:
    """собираем унарный знак в один +/-
    Args: sign_chain - строка с -/+
    Returns: +/-"""

    minus_count: int = sign_chain.count("-")
    return "-" if minus_count % 2 != 0 else "+"


def tokenize(line: str) -> list[str]:
    """разделяет строку на токены и обрабатывает унарные знаки
    Args: line - исходная строка
    Returns: Список токенов"""
    validation.validation_of_input_characters(line)
    start_tokens: list[str] = findall(constants.REGULAR_EXPRESSION, line)
    if not start_tokens:
        raise errors.CalculatorSyntaxError("Ошибка: выражения нет.")

    # валидация
    validation.checking_the_signs_at_the_edges((start_tokens[0], start_tokens[-1]))

    tokens: list[str] = []
    i: int = 0
    while i < len(start_tokens):
        tok: str = start_tokens[i]

        # проверка знаков
        if not (any(char.isdigit() for char in tok) or "." in tok) and any(op in tok
                                                                           for op in constants.ALL_OPERATIONS):

            is_after_operator: bool = (
                (start_tokens[i - 1] if i > 0 else None) in constants.ALL_OPERATIONS or
                (start_tokens[i - 1] if i > 0 else None) == constants.OPEN_PARENTHESIS
            )

            # если после знаков первого приоритета идет -/+
            if (i == 0 or is_after_operator) and all(c in constants.SECOND_PRIORITY_OPERATIONS for c in tok):
                if i + 1 < len(start_tokens):
                    collapse_sign: str = collapse_unar_signs(tok)
                    next_tok: str = start_tokens[i + 1]
                    if collapse_sign == "-":
                        tokens.append(f"-{next_tok}")
                    else:
                        tokens.append(next_tok)
                    i += 2
                    continue

            if any(op in tok for op in constants.FIRST_PRIORITY_OPERATIONS):
                ind_s: str = ""
                ind_e: str = ""
                for ind, char in enumerate(tok):
                    if char in constants.SECOND_PRIORITY_OPERATIONS and ind > 0:
                        ind_s = tok[:ind]
                        ind_e = tok[ind:]
                        break
                if ind_s and ind_e and all(c in constants.SECOND_PRIORITY_OPERATIONS for c in ind_e):
                    tokens.append(ind_s)
                    if i + 1 < len(start_tokens):
                        collapse_sign = collapse_unar_signs(ind_e)
                        next_tok = start_tokens[i + 1]
                        if collapse_sign == "-":
                            tokens.append(f"-{next_tok}")
                        else:
                            tokens.append(next_tok)
                        i += 2
                        continue

            if all(c in constants.SECOND_PRIORITY_OPERATIONS for c in tok):
                tokens.append(collapse_unar_signs(tok))
                i += 1
                continue

            validation.check_sign(tok)
        tokens.append(tok)
        i += 1

    return tokens


def evaluate_flag(tokens: list[str]) -> str:
    """Вычисляет выражение без скобок с учетом приоритетов операции
    Args: tokens - список токенов выражения без скобок
    Returns: результат вычисления"""
    if not tokens:
        return "0"

    currnet_tokens: list[str] = list(tokens)

    # первый приоритет
    i: int = 0
    while i < len(currnet_tokens):
        token: str = currnet_tokens[i]
        if token in constants.FIRST_PRIORITY_OPERATIONS:
            if i == 0 or i == len(currnet_tokens) - 1:
                raise errors.CalculatorSyntaxError("Ошибка: знак находиться с краю")

            num_one: str = currnet_tokens[i - 1]
            num_two: str = currnet_tokens[i + 1]
            result: str = calculation.determination_of_the_sign(num_one, num_two, token)

            currnet_tokens[i - 1:i + 2] = [result]
            i -= 1
        else:
            i += 1

    # второй приоритет
    i = 0
    while i < len(currnet_tokens):
        token = currnet_tokens[i]
        if token in constants.SECOND_PRIORITY_OPERATIONS:
            if i == 0 or i == len(currnet_tokens) - 1:
                raise errors.CalculatorSyntaxError( "Ошибка: знак находиться с краю")

            num_one = currnet_tokens[i - 1]
            num_two = currnet_tokens[i + 1]
            result = calculation.determination_of_the_sign(num_one, num_two, token)

            currnet_tokens[i - 1:i + 2] = [result]
            i -= 1
        else:
            i += 1
    if len(currnet_tokens) > 1:
        raise errors.RandomError()
    return currnet_tokens[0]


def write_json(start_expression: str, result_expression: str) -> None:
    data: dict[str, str] = {
        "expression": start_expression,
        "result": result_expression
    }

    with open("config.json", mode="w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def tokenization(line: str) -> str:
    """точка входа для токенизации и счета
    Args: line - исходное выражение
    Returns: строка с посчитаным значением"""
    tokens: list[str] = tokenize(line)

    tokens_json: list[str] = tokens.copy()

    while constants.OPEN_PARENTHESIS in tokens:
        open_ind = -1
        close_ind = -1

        for ind, token in enumerate(tokens):
            if token == constants.OPEN_PARENTHESIS:
                open_ind = ind
            elif token == constants.CLOSE_PARENTHESIS:
                close_ind = ind
                break

        if open_ind == -1 or close_ind == -1 or open_ind > close_ind:
            raise errors.CalculatorParenthesisError("Ошибка: скобки некорректно расположены.")

        #подвыражение внутри скобок
        sub_exp: list[str] = tokens[open_ind + 1:close_ind]
        sub_res: str = evaluate_flag(sub_exp)

        tokens[open_ind:close_ind + 1] = [sub_res]

    if constants.CLOSE_PARENTHESIS in tokens:
        raise errors.CalculatorParenthesisError("Ошибка: скобки некорректно расположены.")

    result_num: str = evaluate_flag(tokens)

    write_json("".join(tokens_json), result_num)
    return result_num
