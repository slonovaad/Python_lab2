import os
import logging
from src.print_data import print_data
from src.error_messages import (not_exist_error_message, invalid_arguments_error_message,
                                access_error_message, invalid_option_error_message,
                                wrong_type_error_message, )


def ls_validate(options: list[str], paths: list[str]) -> tuple[bool, bool, str]:
    """
    Функция, реализующая валидацию опций и аргументов команды ls
    :param options: список флагов
    :param paths: список передаваемых путей
    :return: пройдена ли валидация, есть ли ключ -l, путь
    """
    if len(paths) > 1 or len(options) > 1:
        invalid_arguments_error_message("ls")
        return False, False, ""
    if len(paths) == 0:
        path = os.getcwd()
    else:
        path = paths[0]
    if len(options) == 0:
        return True, False, path
    if options[0] == "-l":
        return True, True, path
    invalid_option_error_message("ls", options[0])
    return False, False, ""


def ls(options: list[str], paths: list[str]) -> None:
    """
    Функция, реализующая команду ls
    :param options: список флагов
    :param paths: список передаваемых путей
    :return: Данная функция ничего не возвращает
    """
    validated, details, path = ls_validate(options, paths)
    if not validated:
        return
    if path == "~":
        name = os.path.expanduser("~")
    else:
        name = os.path.abspath(path)
    try:
        content = os.listdir(name)
        content = [os.path.join(name, item) for item in content]
        print_data(content, details)
    except FileNotFoundError:
        not_exist_error_message("ls", "directory", paths[0] if len(paths) > 0 else path)
        return
    except PermissionError:
        access_error_message("ls", "directory", paths[0] if len(paths) > 0 else path)
        return
    except NotADirectoryError:
        wrong_type_error_message("ls", "directory", paths[0] if len(paths) > 0 else path)
        return

    logging.info("Success")
