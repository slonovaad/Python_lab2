import os
import zipfile
import logging
from pathlib import Path
from src.error_messages import (not_exist_error_message, invalid_arguments_error_message,
                                access_error_message, wrong_type_error_message,
                                in_parents_error_message)


def zip_validate(options: list[str], paths: list[str]) -> tuple[bool, str]:
    """
    Функция, реализующая валидацию опций и аргументов команды zip
    :param options: список флагов
    :param paths: список передаваемых путей
    :return: пройдена ли валидация, путь-назначение
    """
    if not (1 <= len(paths) <= 2) or len(options) != 0:
        invalid_arguments_error_message("zip")
        return False, ""
    if len(paths) == 2:
        path = paths[1]
    else:
        if os.path.isdir(paths[0]):
            path = paths[0] + ".zip"
        else:
            path = os.path.splitext(paths[0])[0] + ".zip"
    return True, path


def zip(options: list[str], paths: list[str]) -> None:
    """
    Функция, реализующая команду zip
    :param options: список флагов
    :param paths: список передаваемых путей
    :return: Данная функция ничего не возвращает
    """

    validated, path = zip_validate(options, paths)
    if not validated:
        return

    source = os.path.abspath(paths[0])
    destination = os.path.abspath(path)
    if path[-1] in "/\\":
        destination = os.path.join(destination, os.path.basename(source) + ".zip")

    if not (os.path.exists(source)):
        not_exist_error_message("zip", "directory", paths[0])
        return
    if Path(source) in Path(destination).parents:
        in_parents_error_message("zip", paths[0], paths[1])
        return
    if os.path.splitext(destination)[1] != ".zip":
        wrong_type_error_message("zip", "zip file", paths[1])
        return
    try:
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        with zipfile.ZipFile(destination, mode='w',
                             compression=zipfile.ZIP_DEFLATED) as zf:
            if os.path.isdir(source):
                for current_dir, _, files in os.walk(source):
                    for file in files:
                        abs_path = os.path.join(current_dir, file)
                        zf.write(abs_path, arcname=os.path.relpath(abs_path, source))
            else:
                zf.write(source, arcname=os.path.basename(source))
    except PermissionError:
        if len(paths) == 2:
            access_error_message("zip", "directory or file",
                                 f"{paths[0]} or {paths[1]}", action="read or change")
            return
        if len(paths) == 1:
            access_error_message("zip", "directory", paths[0])
            return

    logging.info("Success")
