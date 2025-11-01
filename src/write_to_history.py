import os.path

from src.constants.constants import HISTORY_LIMIT
from src.get_command_number import get_command_number


def write_to_history(file, input_line) -> None:
    """
    Функция, записывающая введённую команду в файл
    в формате history
    :param file: путь к файлу, в который происходит запись
    :param input_line: строка с командой, которую надо записать
    :return: Данная функция ничего не возвращает
    """
    current_number = get_command_number()

    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as history_file:
            lines = history_file.readlines()
    else:
        lines = []
    lines.append(f"{current_number} {input_line}\n")
    if len(lines) > HISTORY_LIMIT:
        lines = lines[-HISTORY_LIMIT:]
    with open(file, 'w', encoding='utf-8') as history_file:
        history_file.writelines(lines)
