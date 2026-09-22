def search_for_brackets(line: str) -> tuple[list[str], str] | str:
    """Убирает все скобки из выражения,
    если они были и добавляет их в список
    result в логически правильном порядке
    Args: line -> строка с выражением
    Returns: result -> список с выражениями в
    скобках в логически правильном порядке"""
    all_brackets: list[str] = []

    ind_s: int = 0
    ind_e: int = 0
    while True:
        if ind_e >= len(line):
            return (all_brackets, line)
        elif line[ind_e] == ")":
            return "!скобка закрытия есть, но нет скобки открытия!"  # поменяй потом на норм исключение
        elif line[ind_e] == "(":
            ind_s = ind_e + 1
            while True:
                if len(line) == ind_e:
                    return "!скобка не закрылась!"  # поменяй потом на норм исключение
                elif line[ind_e] == ")":
                    all_brackets.append(line[ind_s:ind_e])
                    line = line.replace(line[ind_s:ind_e], "", 1)
                    line = line.replace("()", "!!", 1)
                    ind_s, ind_e = 0, 0
                    break
                elif line[ind_e] == "(":
                    ind_s = ind_e + 1
                ind_e += 1
        ind_e += 1
