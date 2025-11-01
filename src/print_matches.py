import re
from src.constants.colors import Color


def print_matches(lines: list[str], pattern: str, ignor_case, name: str = "") -> bool:
    """
    Функция, находящая и печатающая в строкахсовпадающие с шаблоном фрагменты
    :param lines: Список со строками файла
    :param pattern: Шаблон
    :param ignor_case: Игнорируется ли регистр
    :param name: Имя файла
    :return: Было ли что-либо напечатано
    """
    have_printed = False
    for index, line in enumerate(lines):
        have_printed = False
        printing_ind = 0
        if ignor_case:
            find_iterator = re.finditer(pattern, line, re.IGNORECASE)
        else:
            find_iterator = re.finditer(pattern, line)
        for match in find_iterator:
            if printing_ind == 0:
                if name:
                    print(f"{Color.MAGENTA}{name}{Color.CYAN}: ", end='')
                print(f"{Color.CYAN}{index + 1}: {Color.RESET}", end='')
                have_printed = True
            print(line[printing_ind:match.start()], end='')
            print(f"{Color.RED}{match.group(0)}{Color.RESET}", end='')
            printing_ind = match.end()
        if printing_ind != 0:
            print(line[printing_ind:], end='')
    return have_printed
