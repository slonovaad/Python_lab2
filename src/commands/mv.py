import os
import logging
import shutil
from pathlib import Path
from src.make_reserve_copy import make_reserve_copy
from src.write_to_history import write_to_history
from src.constants.constants import HISTORY_FILE, UNDO_HISTORY_FILE, TRASH_DIRECTORY
from src.error_messages import (not_exist_error_message, invalid_arguments_error_message,
                                access_error_message, in_parents_error_message,
                                is_current_dir_error_message)


def mv(options: list[str], paths: list[str]) -> None:
    """
    Функция, реализующая команду mv
    :param options: список флагов
    :param paths: список передаваемых путей
    :return: Данная функция ничего не возвращает
    """

    if len(options) != 0 or len(paths) != 2:
        invalid_arguments_error_message("mv")
        return

    source = os.path.abspath(paths[0])
    destination = os.path.abspath(paths[1])
    current_dir = os.getcwd()
    if paths[1][-1] in "/\\":
        destination = os.path.join(destination, os.path.basename(source))
    if not (os.path.exists(source)):
        not_exist_error_message("mv", "file or directory", paths[0])
        return
    if (source in [HISTORY_FILE, UNDO_HISTORY_FILE, TRASH_DIRECTORY]
            or Path(TRASH_DIRECTORY) in Path(source).parents):
        access_error_message("mv", "file or directory", paths[0], action="change")
        return
    if (destination in [HISTORY_FILE, UNDO_HISTORY_FILE, TRASH_DIRECTORY]
            or Path(TRASH_DIRECTORY) in Path(destination).parents):
        access_error_message("mv", "file or directory", paths[1], action="change")
        return
    if source == current_dir:
        is_current_dir_error_message("mv", paths[0], action="move")
        return
    if destination == current_dir:
        is_current_dir_error_message("mv", paths[1], action="move")
        return
    if Path(source) in Path(destination).parents:
        in_parents_error_message("mv", paths[0], paths[1])
        return
    if destination == os.path.abspath("/") or destination == os.path.expanduser("~"):
        access_error_message("mv", "directory", paths[1], action="change")
        return
    if source == os.path.abspath("/") or source == os.path.expanduser("~"):
        access_error_message("mv", "directory", paths[0], action="change")
        return
    if not (os.access(source, os.W_OK)):
        access_error_message("mv", "file or directory", paths[0], action="change")
        return
    if os.path.exists(destination):
        if not (os.access(destination, os.W_OK)):
            access_error_message("mv", "file or directory", paths[1], action="change")
            return
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    if os.path.exists(destination):
        make_reserve_copy(destination)
        if os.path.isfile(destination):
            os.remove(destination)
        if os.path.isdir(destination):
            shutil.rmtree(destination)
    os.rename(source, destination)
    write_to_history(UNDO_HISTORY_FILE,
                     f'mv "{source}" "{destination}"')
    logging.info("Success")
