import re


def parse(input_str: str) -> tuple[str, list[str], list[str]]:
    """
    Функция, разбивающая входню строку на части (команда, флаги, пути)
    :param input_str: входная строка, введённая пользователем
    :return: строка - команда, список опций, список путей
    """
    input_str += ' '
    command = re.search(r'(?:\S+)', input_str)
    input_str = input_str[command.span()[1]:]
    parser = re.compile(r'(?P<option>(-{1,2}(?:\w{1,2}) ))|(?P<argument>(("(?:.+?)")|(?:\S+)))')
    tokenizer = re.finditer(parser, input_str)
    options = []
    arguments = []
    for token in tokenizer:
        option = token.group("option")
        argument = token.group("argument")
        if option:
            option = option.replace(' ', '')
            option = option.replace('--', '-')
            if len(option) > 2:
                options += ['-' + option_char for option_char in option[1:]]
            else:
                if option not in options:
                    options.append(option)
        if argument:
            argument = argument.replace('"', "")
            arguments.append(argument)
    return command.group(), options, arguments
