import os

import httpx
import pandas as pd
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable

import diy_bbt.utils as utils

api_key = os.environ["KEY_NASDAQ"]

CREDIT_MENU = {
    "aaabonds, aaa": "US AAA rated bond yield",
    "cbrates, cb": "central bank rates",
    "corbonds, cr": "US corporate bond yield",
    "embonds, em": "emerging markets high yield corporate bond yield",
    "govspr, gs": "government bond spreads",
    "govyld, gy": "government bond yields by country",
    "libor, l": "1 month london interbank offered rate USD",
    "news, n": "latest headlines",
    "tryield, tr": "treasury real yield curve rates",
    "tyield, ty": "treasury yield curve rates",
}


# Helper functions
def help():
    return utils.help(menu=CREDIT_MENU, home=False)


def string():
    return "credit"


# Command functions
def aaabonds():
    data = requests.get(
        f"https://data.nasdaq.com/api/v3/datasets/ML/AAAEY.json?api_key={api_key}"
    )
    df = pd.DataFrame.from_dict(data.json()["dataset"]["data"]).dropna()
    table = PrettyTable()
    table.field_names = ["date", "yield"]
    count = 0
    for row in df.itertuples():
        table.add_row(row[1:])
        count += 1
        if count > 12:
            break

    return f"{str(table)}"


def cbrates():
    response = httpx.get("https://www.investing.com/central-banks/")
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", id="curr_table")
    tr_elements = table.find_all("tbody")[0].find_all("tr")
    data = []
    for tr in tr_elements:
        td_elements = tr.find_all("td")
        row = []
        for td in td_elements:
            row.append(td.text.strip())
        data.append(row)

    table = PrettyTable()
    table.field_names = ["central bank", "current rate", "next meeting", "last change"]
    for row in data:
        table.add_row(utils.format_string(row[1:]))

    table.align["central bank"] = "l"

    return f"{str(table)}"


def corbonds():
    data = requests.get(
        f"https://data.nasdaq.com/api/v3/datasets/ML/USEY.json?api_key={api_key}"
    )
    df = pd.DataFrame.from_dict(data.json()["dataset"]["data"]).dropna()
    table = PrettyTable()
    table.field_names = ["date", "yield"]
    count = 0
    for row in df.itertuples():
        table.add_row(row[1:])
        count += 1
        if count > 12:
            break

    return f"{str(table)}"


def embonds():
    data = requests.get(
        f"https://data.nasdaq.com/api/v3/datasets/ML/EMHYY.json?api_key={api_key}"
    )
    df = pd.DataFrame.from_dict(data.json()["dataset"]["data"]).dropna()
    table = PrettyTable()
    table.field_names = ["date", "yield"]
    count = 0
    for row in df.itertuples():
        table.add_row(row[1:])
        count += 1
        if count > 12:
            break

    return f"{str(table)}"


def govspr():
    response = httpx.get(
        "https://www.investing.com/rates-bonds/government-bond-spreads"
    )
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", id="bonds")
    tr_elements = table.find("tbody").find_all("tr")
    data = []
    for tr in tr_elements:
        td_elements = tr.find_all("td")
        row = []
        for td in td_elements:
            row.append(td.text.strip().replace("+-", "+"))
        data.append(row)

    table = PrettyTable()
    table.field_names = [
        "country",
        "yield",
        "high",
        "low",
        "change",
        "% change",
        "vs. bund",
        "vs. t-note",
        "time",
    ]
    for row in data:
        table.add_row(utils.format_string(row[1:]))

    table = utils.green_red_colouring(table, indices=[4, 5])
    table.align["country"] = "l"

    return f"{str(table)}"


def govyld(country="usa"):
    response = httpx.get(
        f"https://www.investing.com/rates-bonds/{country}-government-bonds"
    )
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", id="cr1")
    tr_elements = table.find("tbody").find_all("tr")
    data = []
    for tr in tr_elements:
        td_elements = tr.find_all("td")
        row = []
        for td in td_elements:
            row.append(td.text.strip().replace("+-", "+"))
        data.append(row)

    table = PrettyTable()
    table.field_names = [
        "name",
        "yield",
        "prev.",
        "high",
        "low",
        "change",
        "% change",
        "time",
    ]
    for row in data:
        table.add_row(utils.format_string(row[1:9]))

    table = utils.green_red_colouring(table, indices=[5, 6])
    table.align["name"] = "l"

    return f"{str(table)}"


def libor():
    response = httpx.get(
        "https://www.marketwatch.com/investing/interestrate/liborusd1m/download-data?countrycode=mr&mod=mw_quote_tab"
    )
    soup = BeautifulSoup(response.content, "html.parser")
    tr_elements = soup.find("tbody", class_="table__body row-hover").find_all("tr")
    data = []
    for tr in tr_elements:
        td_elements = tr.find_all("td")
        row = []
        for td in td_elements:
            content = td.text.strip()
            if "\n" in content:
                content = content.split("\n")[0]
            row.append(content)
        data.append(row)

    table = PrettyTable()
    table.field_names = ["date", "open", "high", "low", "close"]
    for row in data:
        table.add_row(utils.format_string(row))

    return f"{str(table)}"


def news(lim: str = "12"):
    response = httpx.get("https://www.marketwatch.com/investing/bonds")
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.find("div", class_="collection__elements j-scrollElement").find_all(
        "div", class_="article__content"
    )
    data = []
    for x in articles:
        try:
            title = x.find("h3").text.strip()
            if title.startswith("Breaking"):
                title = x.find("a").text.strip()
            data.append([title, x.find("p").text.strip()])
        except Exception:
            pass

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


def tryield():
    data = requests.get(
        f"https://data.nasdaq.com/api/v3/datasets/USTREASURY/REALYIELD.json?api_key={api_key}"
    )
    df = pd.DataFrame.from_dict(data.json()["dataset"]["data"]).dropna()
    table = PrettyTable()
    table.field_names = ["date", "5y", "7y", "10y", "20y", "30y"]
    count = 0
    for row in df.itertuples():
        table.add_row(row[1:])
        count += 1
        if count > 12:
            break

    return f"{str(table)}"


def tyield():
    data = requests.get(
        f"https://data.nasdaq.com/api/v3/datasets/USTREASURY/YIELD.json?api_key={api_key}"
    )
    df = pd.DataFrame.from_dict(data.json()["dataset"]["data"]).dropna()
    table = PrettyTable()
    table.field_names = utils.format_string(data.json()["dataset"]["column_names"])
    count = 0
    for row in df.itertuples():
        table.add_row(row[1:])
        count += 1
        if count > 12:
            break

    return f"{str(table)}"
