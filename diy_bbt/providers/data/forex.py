import os

import httpx
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable

import diy_bbt.utils as utils

api_key = os.environ["KEY_TWELVE_DATA"]

FOREX_MENU = {
    "convert, c": "convert currency amount",
    "rate, r": "single exchange rate",
    "mrate, m": "major exchange rates",
    "news, n": "latest headlines",
    "series, s": "exchange rate time series data",
}


# Helper functions
def help():
    return utils.help(menu=FOREX_MENU, home=False)


def string():
    return "forex"


# Command functions
def convert(symbol="GBP/USD", amount="1"):
    data = requests.get(
        f"https://api.twelvedata.com/currency_conversion?symbol={symbol}&amount={amount}&apikey={api_key}"
    ).json()
    data.pop("symbol", None)
    data.pop("timestamp", None)
    table = PrettyTable()
    for key in data.keys():
        table.add_row([utils.format_string(key), utils.format_float(data[key])])

    table.header = False

    return f"{str(table)}"


def rate(*symbols):
    data = []
    for symbol in symbols:
        data.append(
            requests.get(
                f"https://api.twelvedata.com/exchange_rate?symbol={symbol}&apikey={api_key}"
            ).json()
        )
    table = PrettyTable()
    for item in data:
        table.add_row(
            [utils.format_string(item["symbol"]), utils.format_float(item["rate"])]
        )

    table.header = False

    return f"{str(table)}"


def mrate():
    response = httpx.get(
        "https://www.investing.com/currencies/streaming-forex-rates-majors"
    )
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("tbody")
    tr_elements = table.find_all("tr")
    data = []
    for tr in tr_elements:
        td_elements = tr.find_all("td")
        row = []
        for i, td in enumerate(td_elements):
            content = td.text.strip()
            if i == 0:
                content = content.replace("Layer 1", "")
            row.append(content)
        data.append(row)

    table = PrettyTable()
    table.field_names = ["pair", "bid", "ask", "high", "low", "chg.", "chg. %", "time"]
    for row in data:
        table.add_row(utils.format_string(row))

    table.align["pair"] = "l"
    table = utils.green_red_colouring(table, indices=[5, 6])

    return f"{str(table)}"


def news(lim: str = "12"):
    response = httpx.get("https://www.dailyfx.com/market-news/articles")
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.find("div", class_="dfx-articleList jsdfx-articleList").find_all(
        "a"
    )
    data = []
    for article in articles:
        content = article.find_all()
        data.append([content[1].text.strip(), content[4].text.strip()])

    table = PrettyTable()
    table.field_names = ["title", "description"]
    count = 0
    for row in data:
        table.add_row(row)
        if count > int(lim):
            break
        count += 1

    table._max_width = {"title": 45, "description": 60}
    table.align = "l"

    return f"{str(table)}"


def series(symbol="GBP/USD", interval="1day"):
    data = requests.get(
        f"https://api.twelvedata.com/time_series?symbol={symbol.upper()}&interval={interval}&apikey={api_key}"
    ).json()["values"]
    table = PrettyTable()
    table.field_names = ["date", "open", "high", "low", "close"]
    for item in data:
        vals = list(item.values())
        datetime = utils.format_string(vals[0])
        rates = [utils.format_float(float(x), 4) for x in vals[1:]]
        table.add_row([datetime] + rates)

    return f"{str(table)}"
