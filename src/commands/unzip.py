import os
import zipfile
import logging
from src.error_messages import (not_exist_error_message, invalid_arguments_error_message,
                                access_error_message, wrong_type_error_message, )

def unzip_validate(options: list[str], paths: list[str]) -> bool:
    """
    Функция, реализующая валидацию опций и аргументов команды unzip
    :param options: список флагов
    :param paths: список передаваемых путей
    :return: пройдена ли валидация
    """
    if len(options) != 0 or len(paths) != 1:
        invalid_arguments_error_message("unzip")
        return False
    return True


def unzip(options: list[str], paths: list[str]) -> None:
    """
    Функция, реализующая команду unzip
    :param options: список флагов
    :param paths: список передаваемых путей
    :return: Данная функция ничего не возвращает
    """

    if not (unzip_validate(options, paths)):
        return

    name = os.path.abspath(paths[0])
    if not (os.path.exists(name)):
        not_exist_error_message("unzip", "file", paths[0])
        return
    if not (os.path.isfile(name)):
        wrong_type_error_message("unzip", "file", paths[0])
        return
    if os.path.splitext(name)[1] != ".zip":
        wrong_type_error_message("unzip", "zip file", paths[0])
        return
    try:
        with zipfile.ZipFile(name) as zf:
            zf.extractall(os.getcwd())
    except PermissionError:
        access_error_message("unzip", "file", paths[0])
        return

    logging.info("Success")
