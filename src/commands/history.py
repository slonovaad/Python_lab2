import logging
from src.constants.constants import HISTORY_FILE
from src.error_messages import invalid_arguments_error_message


def history(options: list[str], arguments: list[str]) -> None:
    """
    Функция, реализующая команду history
    :param options: список введённых флагов
    :param arguments: список введённых аргументов
    :return: Данная функция ничего не возвращает
    """
    if len(arguments) > 1 or len(options) != 0:
        invalid_arguments_error_message("history")
        return
    with open(HISTORY_FILE, "r", encoding='utf-8',) as history_file:
        lines = history_file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i][:-1]
    if len(arguments) == 1:
        try:
            number = int(arguments[0])
        except ValueError:
            invalid_arguments_error_message("history")
            return
        print(*lines[(-1) * number:], sep="\n")
    else:
        print(*lines, sep="\n")
    logging.info("Success")
