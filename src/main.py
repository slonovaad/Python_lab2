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
from src.form_printed_path import form_printed_path


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
    while (input_str := input(form_printed_path(home))) != "exit":
        logging.info(input_str)
        try:
            command, options, arguments = parse(input_str)
        except AttributeError:
            logging.info("Blank line")
            continue
        if command in COMMANDS:
            COMMANDS[command](options, arguments)
        else:
            command_not_found_error_message(command)
        write_to_history(HISTORY_FILE, input_str)
    if os.path.exists(TRASH_DIRECTORY):
        shutil.rmtree(TRASH_DIRECTORY)
    if os.path.exists(UNDO_HISTORY_FILE):
        os.remove(UNDO_HISTORY_FILE)


if __name__ == "__main__":
    main()
