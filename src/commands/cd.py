import os
import logging
from src.error_messages import (not_exist_error_message, invalid_arguments_error_message,
                                access_error_message, wrong_type_error_message)


def cd(options: list[str], paths: list[str]) -> None:
    """
    Функция, реализующая команду cd
    :param options: список флагов
    :param paths: список передаваемых путей
    :return: Данная функция ничего не возвращает
    """
    if len(paths) != 1 or len(options) != 0:
        invalid_arguments_error_message("cd")
        return
    name = paths[0]
    if name == '~':
        os.chdir(os.path.expanduser("~"))
        logging.info("Success")
        return
    try:
        os.chdir(os.path.abspath(name))
    except FileNotFoundError:
        not_exist_error_message("cd", "directory", name)
        return
    except PermissionError:
        access_error_message("cd", "directory", name)
        return
    except NotADirectoryError:
        wrong_type_error_message("cd", "directory", name)
        return
    logging.info("Success")
