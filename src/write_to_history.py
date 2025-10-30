import os.path

from src.constants.constants import HISTORY_FILE, HISTORY_LIMIT

def write_to_history(file, input_line) -> None:
    """
    Функция, записывающая введённую команду в файл
    в формате history
    :param file: путь к файлу, в который происходит запись
    :param input_line: строка с командой, которую надо записать
    :return: Данная функция ничего не возвращает
    """
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as history_file:
            lines = history_file.readlines()
    else:
        lines = []
    if len(lines) > 0:
        current_number = int(lines[-1].split()[0]) + 1
    else:
        current_number = 1

    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as history_file:
            lines = history_file.readlines()
    else:
        lines = []
    lines.append(f"{current_number} {input_line}\n")
    if len(lines) > HISTORY_LIMIT:
        lines = lines[len(lines) - HISTORY_LIMIT:]
    with open(file, 'w', encoding='utf-8') as history_file:
        history_file.writelines(lines)
