import os
import tarfile
import logging
from pathlib import Path
from src.error_messages import (not_exist_error_message, invalid_arguments_error_message,
                                access_error_message, wrong_type_error_message,
                                in_parents_error_message, )


def tar_validate(options: list[str], paths: list[str]) -> tuple[bool, str]:
    """
    Функция, реализующая валидацию опций и аргументов команды tar
    :param options: список флагов
    :param paths: список передаваемых путей
    :return: пройдена ли валидация, путь-назначение
    """
    if not (1 <= len(paths) <= 2) or len(options) != 0:
        invalid_arguments_error_message("tar")
        return False, ""
    if len(paths) == 2:
        path = paths[1]
    else:
        if os.path.isdir(paths[0]):
            path = paths[0] + ".tar.gz"
        else:
            path = os.path.splitext(paths[0])[0] + ".tar.gz"
    return True, path


def tar(options: list[str], paths: list[str]) -> None:
    """
    Функция, реализующая команду tar
    :param options: список флагов
    :param paths: список передаваемых путей
    :return: Данная функция ничего не возвращает
    """

    validated, path = tar_validate(options, paths)
    if not validated:
        return

    source = os.path.abspath(paths[0])
    destination = os.path.abspath(path)
    if path[-1] in "/\\":
        destination = os.path.join(destination, os.path.basename(source) + ".tar.gz")
    if not (os.path.exists(source)):
        not_exist_error_message("tar", "directory", paths[0])
        return
    if Path(source) in Path(destination).parents:
        in_parents_error_message("tar", paths[0], paths[1])
        return
    path1, ext1 = os.path.splitext(destination)
    if os.path.splitext(path1)[1] + ext1 != ".tar.gz":
        wrong_type_error_message("tar", "tar.gz file", paths[1])
        return
    try:
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        with tarfile.open(destination, "w:gz") as tf:
            if os.path.isdir(source):
                for current_dir, _, files in os.walk(source):
                    for file in files:
                        abs_path = os.path.join(current_dir, file)
                        tf.add(abs_path, arcname=os.path.relpath(abs_path, source))
            else:
                tf.add(source, arcname=os.path.basename(source))
    except PermissionError:
        if len(paths) == 2:
            access_error_message("tar", "directory or file",
                                 f"{paths[0]} or {paths[1]}", action="read or change")
            return
        if len(paths) == 1:
            access_error_message("tar", "directory", paths[0])
            return

    logging.info("Success")
