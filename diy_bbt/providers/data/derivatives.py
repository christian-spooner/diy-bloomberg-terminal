import os
from datetime import datetime, timedelta

import httpx
import requests
import yahooquery as yq
from bs4 import BeautifulSoup
from prettytable import PrettyTable

import diy_bbt.utils as utils

api_key = os.environ["KEY_POLYGON"]

DERIVATIVES_MENU = {
    "aggregate, a": "open, high, low, close for option symbol",
    "calls, c": "call option chain for ticker",
    "contract, cn": "contract details for option symbol",
    "ema": "exponential moving average for option symbol",
    "macd": "options, moving average convergence/divergence for option symbol",
    "news, n": "latest headlines",
    "puts, p": "put option chain for ticker",
    "rsi": "relative strength index for option symbol",
    "sma": "simple moving average for option symbol",
}


# Helper functions
def help():
    return utils.help(menu=DERIVATIVES_MENU, home=False)


def string():
    return "derivatives"


# Command functions


# Options
def aggregate(
    ticker,
    start=(datetime.utcnow() - timedelta(weeks=4)).date(),
    end=datetime.utcnow().date(),
):
    data = requests.get(
        f"https://api.polygon.io/v2/aggs/ticker/{ticker.upper()}"
        + f"/range/1/day/{str(start)}/{str(end)}?adjusted=true&sort=desc&limit=120&apiKey={api_key}"
    ).json()["results"]
    table = PrettyTable()
    table.field_names = [
        "open",
        "high",
        "low",
        "close",
        "vwap",
        "volume",
        "txns",
        "start",
    ]
    for item in data:
        table.add_row(
            [
                utils.format_float(item["o"]),
                utils.format_float(item["h"]),
                utils.format_float(item["l"]),
                utils.format_float(item["c"]),
                utils.format_float(item["vw"]),
                utils.format_float(item["v"]),
                utils.format_float(item["n"]),
                str(datetime.fromtimestamp(item["t"] / 1000).date()),
            ]
        )

    return f"{str(table)}"


def calls(ticker="msft"):
    data = (
        yq.Ticker(ticker.lower())
        .option_chain.reset_index()
        .drop(labels="symbol", axis=1)
    )
    table = PrettyTable()
    table.field_names = data.columns
    count = 0
    for row in data.itertuples():
        table.add_row([utils.format_int(x) for x in row[1:]])
        count += 1
        if count >= 24:
            break

    table.field_names = [
        "expiration",
        "type",
        "symbol",
        "strike",
        "currency",
        "last price",
        "change",
        "% change",
        "volume",
        "open interest",
        "bid",
        "ask",
        "size",
        "last trade",
        "iv",
        "itm",
    ]

    return f"{str(table)}"


def contract(ticker="EVRI240119C00002500"):
    if not ticker.startswith("O:"):
        ticker = "O:" + ticker

    data = requests.get(
        f"https://api.polygon.io/v3/reference/options/contracts/{ticker.upper()}?apiKey={api_key}"
    ).json()["results"]
    table = PrettyTable()
    for k, v in data.items():
        table.add_row([utils.format_string(k), v])

    table.header = False

    return f"{str(table)}"


def ema(ticker, window=24):
    data = requests.get(
        f"https://api.polygon.io/v1/indicators/ema/{ticker.upper()}?timespan=day&adjusted=true"
        + f"&window={window}&series_type=close&sort=desc&limit=120&apiKey={api_key}"
    ).json()["results"]["values"]
    table = PrettyTable()
    table.field_names = [
        "value",
        "timestamp",
    ]
    for item in data:
        table.add_row(
            [
                utils.format_float(item["value"]),
                str(datetime.fromtimestamp(item["timestamp"] / 1000).date()),
            ]
        )

    return f"{str(table)}"


def macd(ticker, short_window=12, long_window=24, signal_window=8):
    data = requests.get(
        f"https://api.polygon.io/v1/indicators/macd/{ticker.upper()}?timespan=day&adjusted=true"
        + f"&short_window={short_window}&long_window={long_window}&signal_window={signal_window}"
        + f"&series_type=close&sort=desc&limit=120&apiKey={api_key}"
    ).json()["results"]["values"]
    table = PrettyTable()
    table.field_names = [
        "value",
        "signal",
        "histogram",
        "timestamp",
    ]
    for item in data:
        table.add_row(
            [
                utils.format_float(item["value"]),
                utils.format_float(item["signal"]),
                utils.format_float(item["histogram"]),
                str(datetime.fromtimestamp(item["timestamp"] / 1000).date()),
            ]
        )

    return f"{str(table)}"


def news():
    response = httpx.get("https://www.totalderivatives.com/latest-news")
    soup = BeautifulSoup(response.content, "html.parser")
    headlines = [x.text.strip() for x in soup.find_all("h4")]
    description = [y.text.strip() for y in soup.find_all("p", class_="intro")]
    table = PrettyTable()
    table.field_names = ["title", "description"]
    for i in range(min(len(headlines), len(description))):
        table.add_row([headlines[i], description[i]])

    table._max_width = {"title": 45, "description": 60}
    table.align = "l"

    return f"{str(table)}"


def puts(ticker="msft"):
    data = (
        yq.Ticker(ticker.lower())
        .option_chain.reset_index()
        .drop(labels="symbol", axis=1)
    )
    table = PrettyTable()
    table.field_names = data.columns
    count = 0
    for row in data.itertuples():
        if row.optionType == "puts":
            table.add_row([utils.format_int(x) for x in row[1:]])
            count += 1
            if count >= 24:
                break

    table.field_names = [
        "expiration",
        "type",
        "symbol",
        "strike",
        "currency",
        "last price",
        "change",
        "% change",
        "volume",
        "open interest",
        "bid",
        "ask",
        "size",
        "last trade",
        "iv",
        "itm",
    ]

    return f"{str(table)}"


def rsi(ticker, window=12):
    data = requests.get(
        f"https://api.polygon.io/v1/indicators/sma/{ticker.upper()}?timespan=day&adjusted=true"
        + f"&window={window}&series_type=close&sort=desc&limit=120&apiKey={api_key}"
    ).json()["results"]["values"]
    table = PrettyTable()
    table.field_names = [
        "value",
        "timestamp",
    ]
    for item in data:
        table.add_row(
            [
                utils.format_float(item["value"]),
                str(datetime.fromtimestamp(item["timestamp"] / 1000).date()),
            ]
        )

    return f"{str(table)}"


def sma(ticker, window=24):
    data = requests.get(
        f"https://api.polygon.io/v1/indicators/sma/{ticker.upper()}?timespan=day&adjusted=true"
        + f"&window={window}&series_type=close&sort=desc&limit=120&apiKey={api_key}"
    ).json()["results"]["values"]
    table = PrettyTable()
    table.field_names = [
        "value",
        "timestamp",
    ]
    for item in data:
        table.add_row(
            [
                utils.format_float(item["value"]),
                str(datetime.fromtimestamp(item["timestamp"] / 1000).date()),
            ]
        )

    return f"{str(table)}"


# Swaps
# TODO

# Futures
# TODO
