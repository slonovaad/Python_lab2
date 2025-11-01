import os
import shutil
import logging
from pathlib import Path
from src.constants.constants import UNDO_HISTORY_FILE, HISTORY_FILE, TRASH_DIRECTORY
from src.make_reserve_copy import make_reserve_copy
from src.write_to_history import write_to_history
from src.error_messages import (not_exist_error_message, invalid_arguments_error_message,
                                access_error_message, invalid_option_error_message,
                                wrong_type_error_message, in_parents_error_message)


def cp(options: list[str], paths: list[str]) -> None:
    """
    Функция, реализующая команду cp
    :param options: список флагов
    :param paths: список передаваемых путей
    :return: Данная функция ничего не возвращает
    """
    if len(paths) != 2 or len(options) > 1:
        invalid_arguments_error_message("cp")
        return
    source = os.path.abspath(paths[0])
    destination = os.path.abspath(paths[1])
    if (destination in [HISTORY_FILE, UNDO_HISTORY_FILE, TRASH_DIRECTORY]
            or Path(TRASH_DIRECTORY) in Path(destination).parents):
        access_error_message("cp", "file or directory", paths[1], action="change")
        return
    if Path(source) in Path(destination).parents:
        in_parents_error_message("cp", paths[0], paths[1])
        return
    if not (os.path.exists(source)):
        not_exist_error_message("cp", "file or directory", paths[0])
        return
    if len(options) == 0:
        if not (os.path.isfile(source)):
            wrong_type_error_message("cp", "file", paths[0])
            print("To copy a directory use -r")
            return

        if paths[1][-1] in '/\\':
            destination = os.path.join(destination, os.path.basename(source))

        try:
            if os.path.exists(destination):
                make_reserve_copy(destination)
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            shutil.copy(source, destination)
        except PermissionError:
            access_error_message("cp", "file or directory",
                                 f"{paths[0]} or {paths[1]}", action="read or change")
            return

    if len(options) == 1:
        option = options[0]
        if option != '-r':
            invalid_option_error_message("cp", option)
            return
        if not (os.path.isdir(source)):
            wrong_type_error_message("cp", "directory", paths[0])
            print("To copy a file don't use -r")
            return
        try:
            if paths[1][-1] not in '/\\':
                if os.path.isdir(destination):
                    destination = os.path.join(destination, os.path.basename(source))
            if os.path.exists(destination):
                make_reserve_copy(destination)
            os.makedirs(destination, exist_ok=True)
            shutil.copytree(source, destination, dirs_exist_ok=True)
        except PermissionError:
            access_error_message("cp", "directory", f"{paths[0]} or {paths[1]}",
                                 action="read or change")
            return
    write_to_history(UNDO_HISTORY_FILE,
                     f'cp "{source}" "{destination}"')
    logging.info("Success")
