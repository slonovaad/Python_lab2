import os
from datetime import datetime


def print_data(files: list[str], details: bool = False) -> None:
    """
    Функция, печатающая данные файлов из списка
    название, опционально: размер, время изменения, права доступа
    :param files: список с названиями файлов, данные о которых необходимо вывести
    :param details: печатать ли детали
    (размер, время изменения, права доступа)
    :return: Данная функция ничего не возвращает
    """
    for item in files:
        size = os.path.getsize(item)
        if os.path.isdir(os.path.join(os.getcwd(), item)):
            print(f'\033[34m{os.path.basename(item).ljust(50, ' ')}\033[0m', end ='')
        else:
            print(os.path.basename(item).ljust(50, ' '), end='')
        if details:
            change_time = datetime.fromtimestamp(os.path.getmtime(item)).strftime('%Y-%m-%d %H:%M')
            rights = os.stat(item).st_mode
            print(f"{str(size).ljust(10, ' ')}   {change_time}   {rights}")
        else:
            print()
