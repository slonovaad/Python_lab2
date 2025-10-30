import logging


def write_error_message(message: str) -> None:
    """Функция, которая выводит сообщение об ошибке
    и записывает его в лог"""
    print(message)
    logging.error(message)


def command_not_found_error_message(command: str) -> None:
    """Сообщение об ошибке, если такой команды нет"""
    write_error_message(f"{command}: Command not found")


def not_exist_error_message(command: str, f_type: str, name: str) -> None:
    """Сообщение об ошибке, если файл/директория не существуют"""
    write_error_message(f"{command}: No such {f_type}: {name}")


def invalid_arguments_error_message(command: str) -> None:
    """Сообщение об ошибке, если передано неверное количество опций/путей"""
    write_error_message(f"{command}: Invalid arguments")


def access_error_message(command: str, f_type: str, name: str, action: str = "read") -> None:
    """Сообщение об ошибке, если нет прав доступа"""
    write_error_message(f"{command}: Not allowed to {action} {f_type}: {name}")


def invalid_option_error_message(command: str, option: str) -> None:
    """Сообщение об ошибке, если такой опции у команды нет"""
    write_error_message(f"{command}: Invalid option {option}")


def wrong_type_error_message(command: str, f_type: str, name: str) -> None:
    """Сообщение об ошибке, если передаваемый путь
    не соответствует ожидаемому типу (файл/директория)"""
    write_error_message(f"{command}: {name}: Is not a {f_type}")


def decode_error_message(command: str, name: str) -> None:
    """Сообщение об ошибке, если не удаётся прочитать файл"""
    write_error_message(f"{command}: Can not decode file: {name}")


def in_parents_error_message(command: str, source: str, target: str) -> None:
    """Сообщение об ошибке, если целевой путь находится внутри исходного"""
    write_error_message(f"{command}: {source} is parent of {target}")


def is_current_dir_error_message(command: str, path: str, action: str) -> None:
    """Сообщение об ошибке, если целевой путь находится внутри исходного"""
    write_error_message(f"{command}: Can not {action}: {path} is current directory")
