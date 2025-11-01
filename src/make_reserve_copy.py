import os
import shutil
from src.constants.constants import TRASH_DIRECTORY
from src.get_command_number import get_command_number


def make_reserve_copy(path) -> None:
    """
    Функция, создающая временную резервную копию
    файла или директории
    :param path: путь к файлу или директории
    :return: Данная функция ничего не возвращает
    """
    if not(os.path.exists(TRASH_DIRECTORY)):
        os.makedirs(TRASH_DIRECTORY)
    current_number = get_command_number()
    new_path = os.path.join(TRASH_DIRECTORY, f"{current_number}_" + os.path.basename(path))
    if os.path.isfile(path):
        shutil.copy(path, new_path)
    elif os.path.isdir(path):
        shutil.copytree(path, new_path)
