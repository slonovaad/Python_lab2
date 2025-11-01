import os
import logging
import shutil
from pathlib import Path
from src.constants.constants import HISTORY_FILE, UNDO_HISTORY_FILE, TRASH_DIRECTORY
from src.make_reserve_copy import make_reserve_copy
from src.write_to_history import write_to_history
from src.error_messages import (not_exist_error_message, invalid_arguments_error_message,
                                access_error_message, wrong_type_error_message,
                                invalid_option_error_message, in_parents_error_message,
                                is_current_dir_error_message)


def rm_validate(options: list[str], paths: list[str]) -> tuple[bool, bool]:
    """
    Функция, реализующая валидацию опций и аргументов команды rm
    :param options: список флагов
    :param paths: список передаваемых путей
    :return: пройдена ли валидация, есть ли ключ -r
    """
    if len(paths) != 1 or len(options) > 1:
        invalid_arguments_error_message("rm")
        return False, False
    if len(options) == 0:
        return True, False
    if options[0] == "-r":
        return True, True
    invalid_option_error_message("rm", options[0])
    return False, False


def rm(options: list[str], paths: list[str]) -> None:
    """
    Функция, реализующая команду rm
    :param options: список флагов
    :param paths: список передаваемых путей
    :return: Данная функция ничего не возвращает
    """

    validated, recursive = rm_validate(options, paths)
    if not validated:
        return

    name = os.path.abspath(paths[0])
    if not (os.path.exists(name)):
        not_exist_error_message("rm", "file or directory", paths[0])
        return

    if Path(name) in Path(os.getcwd()).parents:
        in_parents_error_message("rm", paths[0], "current directory")
        return

    if name == os.getcwd():
        is_current_dir_error_message("rm", paths[0], "remove")
        return

    if name == os.path.abspath("/"):
        access_error_message("rm", "directory", paths[0], action="remove")
        return

    if (name in [HISTORY_FILE, UNDO_HISTORY_FILE, TRASH_DIRECTORY]
            or Path(TRASH_DIRECTORY) in Path(name).parents):
        access_error_message("rm", "file or directory", paths[0], action="remove")
        return

    if not (recursive):
        if not (os.path.isfile(name)):
            wrong_type_error_message("rm", "file", paths[0])
            print("To remove a directory use -r")
            return
        try:
            make_reserve_copy(name)
            os.remove(name)
        except PermissionError:
            access_error_message("rm", "file", paths[0], action="remove")
            return
    else:
        if not (os.path.isdir(name)):
            wrong_type_error_message("rm", "directory", paths[0])
            print("To remove a file don't use -r")
            return
        confirmation = input("Are you sure you want to remove this directory? [y/n] ")
        if confirmation in "Yy":
            try:
                make_reserve_copy(name)
                shutil.rmtree(name)
            except PermissionError:
                access_error_message("rm", "directory", paths[0], action="remove")
                return
        else:
            logging.info("Didn't confirmated")
            return
    write_to_history(UNDO_HISTORY_FILE,
                     f'rm "{name}"')
    logging.info("Success")
