from enum import StrEnum


class Color(StrEnum):
    """Цвета для вывода"""
    RED = "\033[31m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"
    RESET = "\033[0m"
