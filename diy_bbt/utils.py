import colorama
from prettytable import PrettyTable


def help(menu, home=False):
    table = PrettyTable()
    table.field_names = ["Command", "Description"]
    table.align = "l"
    table.header = False
    if not home:
        for command, description in menu.items():
            table.add_row([command, description])
    else:
        for command, description in menu.items():
            table.add_row([command, description])
            if command == "news, n":
                table.add_row(["------------------", ""])
            elif command == "technical, t":
                table.add_row(["------------------", ""])

    return f"{str(table)}"


def format_int(n):
    if isinstance(n, float) or isinstance(n, int):
        return "{:,.0f}".format(n)
    else:
        return n


def format_float(n, i=2):
    if isinstance(n, int) and not isinstance(n, bool):
        return "{:,.0f}".format(n)
    elif isinstance(n, float):
        return "{:,.{}f}".format(n, i)
    else:
        return n


def format_string(strings):
    def do_formatting(string):
        if isinstance(string, str):
            words = []
            current_word = ""
            for i, c in enumerate(string):
                if i == 0 or i == len(string) - 1:
                    current_word += c
                else:
                    if (
                        c.isupper()
                        and current_word
                        and (string[i + 1].islower() or string[i - 1].islower())
                    ):
                        words.append(current_word)
                        current_word = ""
                    elif c == "_":
                        words.append(current_word)
                        current_word = ""
                        continue
                    current_word += c
            words.append(current_word.strip())

            return " ".join(words).lower()
        else:
            return string

    if isinstance(strings, str):
        return do_formatting(strings)
    elif isinstance(strings, list):
        return [do_formatting(string) for string in strings]
    else:
        return strings


def get_elements_before_dash(lst):
    for i, elem in enumerate(lst):
        if elem.startswith("-"):
            return lst[:i]
    return lst


def get_elements_after_dash(lst):
    for i, elem in enumerate(lst):
        if elem.startswith("-"):
            return lst[i:]
    return []


def color_value(value: str, format_str: str = "{:,.2f}") -> str:
    value = value.replace(",", "")
    if not value:
        return value

    if "%" in value:
        value = value.replace("%", "")
        format_str = format_str + "%"

        try:
            float(value)
        except ValueError:
            return value

        if float(value) < 0:
            return (
                colorama.Fore.RED
                + format_str.format(float(value))
                + colorama.Style.RESET_ALL
            )
        if float(value) > 0:
            return (
                colorama.Fore.GREEN
                + format_str.format(float(value))
                + colorama.Style.RESET_ALL
            )
        return value
    else:
        try:
            float(value)
        except ValueError:
            return value

        if float(value) < 0:
            return (
                colorama.Fore.RED
                + format_str.format(float(value))
                + colorama.Style.RESET_ALL
            )
        if float(value) > 0:
            return (
                colorama.Fore.GREEN
                + format_str.format(float(value))
                + colorama.Style.RESET_ALL
            )
        return value


def green_red_colouring(table: PrettyTable, indices: list[int]) -> PrettyTable:
    for row in table.rows:
        row[:] = [
            color_value(row[i]) if i in indices else row[i] for i in range(len(row))
        ]
    return table
