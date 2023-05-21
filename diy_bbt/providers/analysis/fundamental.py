import os
from datetime import datetime, timedelta

import httpx
import yahooquery as yq
from bs4 import BeautifulSoup
from prettytable import PrettyTable

import diy_bbt.utils as utils

api_key = os.environ["KEY_TWELVE_DATA"]

FUNDAMENTAL_MENU = {
    "balance, bl": "balance sheet",
    "cashflow, c": "cashflow statement",
    "comp, cm": "competitors",
    "dividends, dv": "dividend history",
    "earndates, ed": "earnings dates and expectations",
    "earnhist, eh": "historical earnings",
    "earntrend, et": "earnings trends",
    "esg": "environmental, social and governance metrics",
    "financials, f": "financial KPIs",
    "holdmajor, hm": "major share holders",
    "income, i": "income statement",
    "keystats, k": "key statistics",
}


# Helper functions
def help():
    return utils.help(menu=FUNDAMENTAL_MENU, home=False)


def string():
    return "fundamental"


def replace_headers(table: PrettyTable):
    headers = table.rows[0][1:]
    table.field_names = [""] + [t.date() for t in headers]
    table.del_row(0)
    return table


# controllers
def balance(ticker):
    data = yq.Ticker(ticker).balance_sheet().T.iloc[:, ::-1].reset_index()
    data.columns = range(0, len(data.columns))
    data[0] = data[0].str.replace(r"(?<!L)and(?!s)", "And")
    table = PrettyTable()
    table.field_names = data.columns
    for row in data.itertuples():
        table.add_row([utils.format_string(utils.format_int(x)) for x in row[1:]])

    table = replace_headers(table)
    table.align[""] = "l"

    return f"{str(table)}"


def cashflow(ticker):
    data = yq.Ticker(ticker).cash_flow().T.iloc[:, ::-1].reset_index()
    data.columns = range(0, len(data.columns))
    table = PrettyTable()
    table.field_names = data.columns
    for row in data.itertuples():
        table.add_row([utils.format_string(utils.format_int(x)) for x in row[1:]])

    table = replace_headers(table)
    table.align[""] = "l"

    return f"{str(table)}"


def comp(*args, options=()):
    ticker = args[0]
    if "-l" in options:
        lim = int(options[options.index("-l") + 1])
    else:
        lim = 12

    response = httpx.get(
        f"https://csimarket.com/stocks/competition2.php?code={ticker.upper()}"
    )
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", class_="osnovna_tablica_bez_gifa").find_all("tr")
    data = []
    for row in table[1:]:
        data.append([x.text.strip() for x in row.find_all("td")])

    table = PrettyTable()
    table.field_names = [
        "name",
        "q",
        "ticker",
        "revenue",
        "net income",
        "net margin",
        "cash flow",
    ]
    count = 0
    for row in data:
        table.add_row(row)
        if count > lim:
            break
        count += 1

    table.del_column("q")
    table.align["name"] = "l"

    return f"{str(table)}"


def dividends(ticker):
    data = (
        yq.Ticker(ticker)
        .dividend_history(start=datetime.utcnow().date() - timedelta(weeks=360))
        .reset_index()
        .drop(labels="symbol", axis=1)
        .iloc[::-1]
    )
    table = PrettyTable()
    table.field_names = data.columns
    for row in data.itertuples():
        table.add_row([utils.format_float(x) for x in row[1:]])

    return f"{str(table)}"


def earndates(ticker):
    data = yq.Ticker(ticker).earnings[ticker.lower()]["earningsChart"]["quarterly"]
    table = PrettyTable()
    table.field_names = ["date", "actual", "estimate"]
    for row in data:
        table.add_row([utils.format_float(x, 2) for x in list(row.values())])

    return f"{str(table)}"


def earnhist(ticker):
    data = yq.Ticker(ticker).earning_history.iloc[::-1]
    del data["maxAge"]
    table = PrettyTable()
    table.field_names = utils.format_string(list(data.columns))
    for row in data.itertuples():
        table.add_row([utils.format_float(x) for x in row[1:]])

    return f"{str(table)}"


def earntrend(ticker):
    data = yq.Ticker(ticker).earnings_trend[ticker.lower()]["trend"]
    table = PrettyTable()
    table.field_names = list(data[0].keys())[:-1][1:]
    for row in data:
        row["earningsEstimate"] = row["earningsEstimate"]["avg"]
        row["revenueEstimate"] = row["revenueEstimate"]["avg"]
        row["epsTrend"] = row["epsTrend"]["current"]
        row.pop("maxAge")
        row.pop("epsRevisions")
        table.add_row([utils.format_float(x, 2) for x in list(row.values())])

    table.field_names = utils.format_string(table.field_names)

    return f"{str(table)}"


def esg(ticker):
    data = yq.Ticker(ticker).esg_scores[ticker.lower()]
    del data["maxAge"]
    table = PrettyTable()
    for row in data.items():
        table.add_row(
            [
                utils.format_string(row[0]),
                utils.format_float(row[1])
                if not isinstance(row[1], dict)
                else utils.format_float(row[1]["avg"]),
            ]
        )

    table.align["Field 1"] = "l"
    table.header = False

    return f"{str(table)}"


def financials(ticker):
    data = yq.Ticker(ticker).financial_data[ticker.lower()]
    data.pop("maxAge", None)
    table = PrettyTable()
    for row in data.items():
        table.add_row([utils.format_string(row[0]), utils.format_float(row[1])])

    table.align["Field 1"] = "l"
    table.header = False

    return f"{str(table)}"


def holdmajor(ticker):
    data = yq.Ticker(ticker).major_holders[ticker.lower()]
    del data["maxAge"]
    table = PrettyTable()
    for row in data.items():
        table.add_row([utils.format_string(row[0]), utils.format_float(row[1])])

    table.align["Field 1"] = "l"
    table.header = False

    return f"{str(table)}"


def income(ticker):
    data = yq.Ticker(ticker).income_statement().T.iloc[:, ::-1].reset_index()
    data.columns = range(0, len(data.columns))
    table = PrettyTable()
    table.field_names = data.columns
    for row in data.itertuples():
        table.add_row([utils.format_string(utils.format_int(x)) for x in row[1:]])

    table = replace_headers(table)
    table.align[""] = "l"

    return f"{str(table)}"


def keystats(ticker):
    data = yq.Ticker(ticker).key_stats[ticker.lower()]
    del data["maxAge"]
    table = PrettyTable()
    for row in data.items():
        table.add_row([utils.format_string(row[0]), utils.format_float(row[1])])

    table.align["Field 1"] = "l"
    table.header = False

    return f"{str(table)}"
