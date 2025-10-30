import os
import logging
import re
import shutil

from src.constants.constants import UNDO_HISTORY_FILE, TRASH_DIRECTORY
from src.parse import parse
from src.error_messages import invalid_arguments_error_message, not_exist_error_message


def undo(options: list[str], arguments: list[str]) -> None:
    """
    Функция, реализующая команду undo
    :param options: список введённых флагов
    :param arguments: список введённых аргументов
    :return: Данная функция ничего не возвращает
    """
    if len(arguments) != 0 or len(options) != 0:
        invalid_arguments_error_message("undo")
        return
    if not(os.path.exists(UNDO_HISTORY_FILE)):
        not_exist_error_message("undo",
                                "commands in history", "cp, mv, rm")
        return

    with open(UNDO_HISTORY_FILE, "r", encoding="utf-8") as history_file:
        lines = history_file.readlines()

    if len(lines) == 0:
        not_exist_error_message("undo",
                                "commands in history", "cp, mv, rm")
        return
    line = lines[-1]
    number = re.search(r"\d+", line).group()
    line_without_number = re.sub(r'\d+ ', '', line, count=1)
    command, _, paths = parse(line_without_number)

    if command == "cp":
        name = os.path.abspath(paths[1])
        if os.path.isfile(name):
            os.remove(name)
        if os.path.isdir(name):
            shutil.rmtree(name)
        recovering_path = os.path.join(TRASH_DIRECTORY, f"{number}_" + os.path.basename(name))
        if os.path.exists(recovering_path):
            if os.path.isfile(recovering_path):
                shutil.copy(recovering_path, name)
                os.remove(recovering_path)
            if os.path.isdir(recovering_path):
                shutil.copytree(recovering_path, name)
                shutil.rmtree(recovering_path)
    if command == "mv":
        source = os.path.abspath(paths[0])
        destination = os.path.abspath(paths[1])
        os.rename(destination, source)
        recovering_path = os.path.join(TRASH_DIRECTORY, f"{number}_" + os.path.basename(destination))
        if os.path.exists(recovering_path):
            if os.path.isfile(recovering_path):
                shutil.copy(recovering_path, destination)
                os.remove(recovering_path)
            if os.path.isdir(recovering_path):
                shutil.copytree(recovering_path, destination)
                shutil.rmtree(recovering_path)
    if command == "rm":
        name = os.path.abspath(paths[0])
        recovering_path = os.path.join(TRASH_DIRECTORY, f"{number}_" + os.path.basename(name))
        if os.path.exists(recovering_path):
            if os.path.isfile(recovering_path):
                shutil.copy(recovering_path, name)
                os.remove(recovering_path)
            if os.path.isdir(recovering_path):
                shutil.copytree(recovering_path, name)
                shutil.rmtree(recovering_path)

    with open(UNDO_HISTORY_FILE, "w", encoding="utf-8") as history_file:
        history_file.writelines(lines[:-1])

    logging.info("Success")
