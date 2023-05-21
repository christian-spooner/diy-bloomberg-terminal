import os

from prettytable import PrettyTable

import diy_bbt.utils as utils

SETTINGS_MENU = {
    "keys, k": "view api keys",
}


# Helper functions
def help():
    return utils.help(menu=SETTINGS_MENU, home=False)


def string():
    return "settings"


# Command functions
def keys():
    data = {key: val for key, val in dict(os.environ).items() if key.startswith("KEY")}
    table = PrettyTable()
    for k, v in data.items():
        table.add_row([k[4:], v])

    table.header = False
    table.align = "l"

    return f"{str(table)}"
