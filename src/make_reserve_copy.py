import os
import shutil
from src.constants.constants import HISTORY_FILE, TRASH_DIRECTORY


def make_reserve_copy(path) -> None:
    """
    Функция, создающая временную резервную копию
    файла или директории
    :param path: путь к файлу или директории
    :return: Данная функция ничего не возвращает
    """
    if not(os.path.exists(TRASH_DIRECTORY)):
        os.makedirs(TRASH_DIRECTORY)
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as history_file:
            lines = history_file.readlines()
        current_number = int(lines[-1].split()[0]) + 1
    else:
        current_number = 1
    new_path = os.path.join(TRASH_DIRECTORY, f"{current_number}_" + os.path.basename(path))
    if os.path.isfile(path):
        shutil.copy(path, new_path)
    elif os.path.isdir(path):
        shutil.copytree(path, new_path)
