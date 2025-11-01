import os
import logging
from src.error_messages import (not_exist_error_message, invalid_arguments_error_message,
                                access_error_message, wrong_type_error_message)


def cat_validate(options: list[str], paths: list[str]) -> bool:
    """
    Функция, реализующая валидацию опций и аргументов команды cat
    :param options: список флагов
    :param paths: список передаваемых путей
    :return: пройдена ли валидация
    """
    if len(paths) != 1 or len(options) != 0:
        invalid_arguments_error_message("cat")
        return False
    return True


def cat(options: list[str], paths: list[str]) -> None:
    """
    Функция, реализующая команду cat
    :param options: список флагов
    :param paths: список передаваемых путей
    :return: Данная функция ничего не возвращает
    """
    if not (cat_validate(options, paths)):
        return
    if len(paths) != 1 or len(options) != 0:
        invalid_arguments_error_message("cat")
        return
    name = os.path.abspath(paths[0])
    if not (os.path.exists(name)):
        not_exist_error_message("cat", "file", paths[0])
        return
    if not (os.path.isfile(name)):
        wrong_type_error_message("cat", "file", paths[0])
        return
    try:
        with open(name, "rb") as file:
            print(file.read().decode())
    except PermissionError:
        access_error_message("cat", "file", paths[0])
        return
    except UnicodeDecodeError:
        with open(name, "rb") as file:
            print(file.read())
    logging.info("Success")
