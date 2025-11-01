import os
from pathlib import Path


def form_printed_path(home: os.PathLike[str]) -> str:
    """
        Функция, разбивающая входню строку на части (команда, флаги, пути)
        :param home: домашняя директория
        :return: выводимый путь к текущей директории
    """
    current_dir = Path(os.path.abspath(os.getcwd()))
    if home in current_dir.parents:
        printed_path = f"\033[32m{home}\033[0m:\033[34m{
        os.path.relpath(current_dir, start=home)}\033[0m> "
    else:
        printed_path = f"\033[32m{current_dir}\033[0m> "

    return printed_path
