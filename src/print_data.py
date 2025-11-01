import os
from datetime import datetime
from src.constants.colors import Color


def print_data(files: list[str], details: bool = False) -> None:
    """
    Функция, печатающая данные файлов из списка
    название, опционально: размер, время изменения, права доступа
    :param files: список с названиями файлов, данные о которых необходимо вывести
    :param details: печатать ли детали
    (размер, время изменения, права доступа)
    :return: Данная функция ничего не возвращает
    """
    message = ""
    for item in files:
        size = os.path.getsize(item)
        if os.path.isdir(os.path.join(os.getcwd(), item)):
            message += f"{Color.BLUE}{os.path.basename(item).ljust(50, ' ')}{Color.RESET}"
        else:
            message += os.path.basename(item).ljust(50, ' ')
        if details:
            change_time = datetime.fromtimestamp(os.path.getmtime(item)).strftime('%Y-%m-%d %H:%M')
            rights = os.stat(item).st_mode
            message += f"{str(size).ljust(10, ' ')}   {change_time}   {rights}"

        message += "\n"
    print(message, end="")
