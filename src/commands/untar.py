import os
import tarfile
import logging
from src.error_messages import (not_exist_error_message, invalid_arguments_error_message,
                                access_error_message, wrong_type_error_message, )


def untar_validate(options: list[str], paths: list[str]) -> bool:
    """
    Функция, реализующая валидацию опций и аргументов команды untar
    :param options: список флагов
    :param paths: список передаваемых путей
    :return: пройдена ли валидация
    """
    if len(options) != 0 or len(paths) != 1:
        invalid_arguments_error_message("untar")
        return False
    return True


def untar(options: list[str], paths: list[str]) -> None:
    """
    Функция, реализующая команду unzip
    :param options: список флагов
    :param paths: список передаваемых путей
    :return: Данная функция ничего не возвращает
    """

    if not(untar_validate(options, paths)):
        return

    name = os.path.abspath(paths[0])
    if not (os.path.exists(name)):
        not_exist_error_message("untar", "file", paths[0])
        return
    if not (os.path.isfile(name)):
        wrong_type_error_message("untar", "file", paths[0])
        return
    path1, ext1 = os.path.splitext(name)
    if os.path.splitext(path1)[1] + ext1 != ".tar.gz":
        wrong_type_error_message("untar", "tar.gz file", paths[0])
        return
    try:
        with tarfile.open(name) as tf:
            tf.extractall()
    except PermissionError:
        access_error_message("untar", "file", paths[0])
        return

    logging.info("Success")
