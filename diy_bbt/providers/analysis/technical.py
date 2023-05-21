import csv
import os

import colorama
import requests
from prettytable import PrettyTable

import diy_bbt.utils as utils

api_key = os.environ["KEY_TWELVE_DATA"]

TECHNICAL_MENU = {
    "indicator, i": "technical indicator time series",
    "indlist, il": "list of available indicators",
}


# Helper functions
def help():
    return utils.help(menu=TECHNICAL_MENU, home=False)


def string():
    return "technical"


# controllers
def indicator(indicator, symbol, interval="1min"):
    data = requests.get(
        f"https://api.twelvedata.com/{indicator}?symbol={symbol}&interval={interval}&apikey={api_key}"
    ).json()["values"]
    table = PrettyTable()
    for item in data:
        table.add_row(
            [
                utils.format_float(float(item[indicator])),
                utils.format_string(item["datetime"]),
            ]
        )

    table.header = False

    return f"{str(table)}"


def indlist():
    INDICATORS = {}
    with open("diy_bbt/storage/files/indicators.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            code, name = row
            INDICATORS[code] = name

    table = PrettyTable()
    for k, v in INDICATORS.items():
        table.add_row(
            [
                colorama.Fore.BLUE + k.lower() + colorama.Style.RESET_ALL,
                v,
            ]
        )

    table._max_width = {"Field 2": 72}
    table.align = "l"
    table.header = False

    return f"{str(table)}"
