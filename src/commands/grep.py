import os
import logging
import re

from src.error_messages import (not_exist_error_message, invalid_arguments_error_message,
                                access_error_message, wrong_type_error_message,
                                decode_error_message, invalid_option_error_message)


def grep(options: list[str], arguments: list[str]) -> None:
    """
    Функция, реализующая команду cat
    :param options: список флагов
    :param arguments: список передаваемых фргументов
    (шаблон и путь)
    :return: Данная функция ничего не возвращает
    """
    if len(arguments) != 2 or len(options) > 2:
        invalid_arguments_error_message("grep")
        return
    if len(options) > 0:
        if options[0] not in ["-i", "-r"]:
            invalid_option_error_message("grep", options[0])
            return
    if len(options) > 1:
        if options[1] not in ["-i", "-r"]:
            invalid_option_error_message("grep", options[1])
            return

    name = os.path.abspath(arguments[1])
    pattern = arguments[0]

    if not (os.path.exists(name)):
        not_exist_error_message("grep", "file or directory", arguments[1])
        return

    if os.path.isfile(name):
        if "-r" in options:
            wrong_type_error_message("grep", "directory", arguments[1])
            print("To work with a file don't use -r")
            return
        try:
            with open(name, "r", encoding="utf-8") as file:
                lines = file.readlines()
            for index, line in enumerate(lines):
                printing_ind = 0
                if "-i" in options:
                    find_iterator = re.finditer(pattern, line, re.IGNORECASE)
                else:
                    find_iterator = re.finditer(pattern, line)
                for match in find_iterator:
                    if printing_ind == 0:
                        print(f"\033[36m{index + 1}: \033[0m", end='')
                    print(line[printing_ind:match.start()], end='')
                    print(f"\033[31m{match.group(0)}\033[0m", end='')
                    printing_ind = match.end()
                if printing_ind != 0:
                    print(line[printing_ind:], end='')
            print()

        except PermissionError:
            access_error_message("grep", "file", name)
            return
        except UnicodeDecodeError:
            decode_error_message("grep", name)

    if os.path.isdir(name):
        if "-r" not in options:
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
                        have_printed = False
                        for index, line in enumerate(lines):
                            have_printed = False
                            printing_ind = 0
                            if "-i" in options:
                                find_iterator = re.finditer(pattern, line, re.IGNORECASE)
                            else:
                                find_iterator = re.finditer(pattern, line)
                            for match in find_iterator:
                                if printing_ind == 0:
                                    print(f"\033[35m{
                                    os.path.relpath(abs_path, start=name)
                                    }\033[36m: {index + 1}: \033[0m", end='')
                                    have_printed = True
                                print(line[printing_ind:match.start()], end='')
                                print(f"\033[31m{match.group(0)}\033[0m", end='')
                                printing_ind = match.end()
                            if printing_ind != 0:
                                print(line[printing_ind:], end='')
                        if have_printed:
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
