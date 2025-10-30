import os
import shutil
import logging
from pathlib import Path
from src.constants.constants import (LOG_FILE, HISTORY_FILE,
                                     UNDO_HISTORY_FILE, TRASH_DIRECTORY)
from src.constants.commands_constants import COMMANDS
from src.error_messages import command_not_found_error_message
from src.parse import parse
from src.write_to_history import write_to_history


def main() -> None:
    """
    Точка входа в приложение. Вызывает функцию,
    соответствующуб введённой в терминал команде.
    :return: Данная функция ничего не возвращает
    """
    logging.basicConfig(level=logging.INFO, filename=LOG_FILE,
                        encoding='utf-8',
                        format="[%(asctime)s] %(levelname)s: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    home = Path(os.path.expanduser("~"))
    while True:
        current_dir = Path(os.path.abspath(os.getcwd()))
        if home in current_dir.parents:
            printed_path = f"\033[32m{home}\033[0m:\033[34m{
            os.path.relpath(current_dir, start=home)}\033[0m> "
        else:
            printed_path = f"\033[32m{current_dir}\033[0m> "
        input_str = input(printed_path)
        logging.info(input_str)
        try:
            command, options, arguments = parse(input_str)
        except AttributeError:
            logging.info("Blank line")
            continue
        if command in COMMANDS:
            COMMANDS[command](options, arguments)
        elif command == "exit":
            write_to_history(HISTORY_FILE, input_str)
            logging.info("Exit")
            break
        else:
            command_not_found_error_message(command)
        write_to_history(HISTORY_FILE, input_str)
    if os.path.exists(TRASH_DIRECTORY):
        shutil.rmtree(TRASH_DIRECTORY)
    if os.path.exists(UNDO_HISTORY_FILE):
        os.remove(UNDO_HISTORY_FILE)


if __name__ == "__main__":
    main()
