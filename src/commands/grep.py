import os
import logging
from src.print_matches import print_matches
from src.error_messages import (not_exist_error_message, invalid_arguments_error_message,
                                access_error_message, wrong_type_error_message,
                                decode_error_message, invalid_option_error_message)


def grep_validate(options: list[str], arguments: list[str]) -> tuple[bool, bool, bool]:
    """
    Функция, реализующая валидацию опций и аргументов команды grep
    :param options: список флагов
    :param arguments: список передаваемых аргументов
    :return: пройдена ли валидация, есть ли ключ -r, есть ли ключ -i
    """
    if len(arguments) != 2 or len(options) > 2:
        invalid_arguments_error_message("grep")
        return False, False, False
    if len(options) > 0:
        if options[0] not in ["-i", "-r"]:
            invalid_option_error_message("grep", options[0])
            return False, False, False
    if len(options) > 1:
        if options[1] not in ["-i", "-r"]:
            invalid_option_error_message("grep", options[1])
            return False, False, False
    return True, "-r" in options, "-i" in options


def grep(options: list[str], arguments: list[str]) -> None:
    """
    Функция, реализующая команду grep
    :param options: список флагов
    :param arguments: список передаваемых аргументов
    (шаблон и путь)
    :return: Данная функция ничего не возвращает
    """
    validated, recursive, ignor_case = grep_validate(options, arguments)
    if not validated:
        return

    name = os.path.abspath(arguments[1])
    pattern = arguments[0]

    if not (os.path.exists(name)):
        not_exist_error_message("grep", "file or directory", arguments[1])
        return

    if os.path.isfile(name):
        if recursive:
            wrong_type_error_message("grep", "directory", arguments[1])
            print("To work with a file don't use -r")
            return
        try:
            with open(name, "r", encoding="utf-8") as file:
                lines = file.readlines()
            print_matches(lines, pattern, ignor_case)
            print()
        except PermissionError:
            access_error_message("grep", "file", name)
            return
        except UnicodeDecodeError:
            decode_error_message("grep", name)

    if os.path.isdir(name):
        if not (recursive):
            wrong_type_error_message("grep", "file", arguments[1])
            print("To work with a directory use -r")
            return
        try:
            for current_dir, _, files in os.walk(name):
                for file in files:
                    abs_path = os.path.join(current_dir, file)
                    try:
                        with open(abs_path, "r",
                                  encoding="utf-8") as reading_file:
                            lines = reading_file.readlines()
                        if print_matches(lines, pattern, ignor_case, os.path.relpath(abs_path, start=name)):
                            print()
                    except PermissionError:
                        print(f"{"grep"} {
                        os.path.relpath(abs_path, start=name)
                        }: Not allowed to read")
                    except UnicodeDecodeError:
                        print(f"{"grep"} {
                        os.path.relpath(abs_path, start=name)
                        }: Can not decode")
        except PermissionError:
            access_error_message("grep", "directory", arguments[1])
            return

    logging.info("Success")
