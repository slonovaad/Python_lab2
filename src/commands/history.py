import logging
from src.constants.constants import HISTORY_FILE
from src.error_messages import invalid_arguments_error_message


def history_validate(options: list[str], arguments: list[str]) -> tuple[bool, int]:
    """
    Функция, реализующая валидацию опций и аргументов команды history
    :param options: список флагов
    :param arguments: список передаваемых путей
    :return: пройдена ли валидация, аргумент (-1, если его нет)
    """
    if len(arguments) > 1 or len(options) != 0:
        invalid_arguments_error_message("history")
        return False, False
    if len(arguments) == 1:
        try:
            number = int(arguments[0])
        except ValueError:
            invalid_arguments_error_message("history")
            return False, False
        if number <= 0:
            invalid_arguments_error_message("history")
            return False, False
        return True, number
    return True, -1


def history(options: list[str], arguments: list[str]) -> None:
    """
    Функция, реализующая команду history
    :param options: список введённых флагов
    :param arguments: список введённых аргументов
    :return: Данная функция ничего не возвращает
    """
    validated, number = history_validate(options, arguments)
    if not validated:
        return
    with open(HISTORY_FILE, "r", encoding='utf-8', ) as history_file:
        lines = history_file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i][:-1]
    if number > 0:
        print(*lines[(-1) * number:], sep="\n")
    else:
        print(*lines, sep="\n")
    logging.info("Success")
