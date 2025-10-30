import os
import logging
from src.print_data import print_data
from src.error_messages import (not_exist_error_message, invalid_arguments_error_message,
                                access_error_message, invalid_option_error_message,
                                wrong_type_error_message, )


def ls(options: list[str], paths: list[str]) -> None:
    """
    Функция, реализующая команду ls
    :param options: список флагов
    :param paths: список передаваемых путей
    :return: Данная функция ничего не возвращает
    """
    if len(paths) == 0:
        if len(options) == 1:
            if options[0] == '-l':
                try:
                    print_data(os.listdir(), details=True)
                except PermissionError:
                    access_error_message("ls", "directory", os.getcwd())
                    return
            else:
                invalid_option_error_message("ls", options[0])
                return
        elif len(options) == 0:
            try:
                print_data(os.listdir())
            except PermissionError:
                access_error_message("ls", "directory", os.getcwd())
                return
        else:
            invalid_arguments_error_message("ls")
            return
    elif len(paths) == 1:
        name = os.path.abspath(paths[0])
        if paths[0] == "~":
            name = os.path.expanduser("~")
        if len(options) == 1:
            if options[0] == '-l':
                try:
                    content = os.listdir(name)
                    content = [os.path.join(name, item) for item in content]
                    print_data(content, details=True)
                except FileNotFoundError:
                    not_exist_error_message("ls", "directory", paths[0])
                    return
                except PermissionError:
                    access_error_message("ls", "directory", paths[0])
                    return
            else:
                invalid_option_error_message("ls", options[0])
                return
        elif len(options) == 0:
            try:
                content = os.listdir(name)
                content = [os.path.join(name, item) for item in content]
                print_data(content)
            except FileNotFoundError:
                not_exist_error_message("ls", "directory", paths[0])
                return
            except PermissionError:
                access_error_message("ls", "directory", paths[0])
                return
            except NotADirectoryError:
                wrong_type_error_message("ls", "directory", paths[0])
                return
        else:
            invalid_arguments_error_message("ls")
            return
    else:
        invalid_arguments_error_message("ls")
        return

    logging.info("Success")
