import os
from pathlib import Path
from src.constants.colors import Color


def form_printed_path(home: os.PathLike[str]) -> str:
    """
        Функция, разбивающая входню строку на части (команда, флаги, пути)
        :param home: домашняя директория
        :return: выводимый путь к текущей директории
    """
    current_dir = Path(os.path.abspath(os.getcwd()))
    if home in current_dir.parents:
        printed_path = f"{Color.GREEN}{home}{Color.RESET}:{Color.BLUE}{
        os.path.relpath(current_dir, start=home)}{Color.RESET}> "
    else:
        printed_path = f"{Color.GREEN}{current_dir}{Color.RESET}> "

    return printed_path
