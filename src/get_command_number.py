import os.path

from src.constants.constants import HISTORY_FILE


def get_command_number() -> int:
    """
    Функция, которая определяет номер последней записанной в историю команды
    :return: Номер команды
    """
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as history_file:
            lines = history_file.readlines()
    else:
        return 1
    if len(lines) > 0:
        return int(lines[-1].split()[0]) + 1
    return 1
