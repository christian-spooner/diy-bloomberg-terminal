import os

import httpx
import matplotlib.pyplot as plt
import mplcursors
import pandas as pd
from bs4 import BeautifulSoup
from fredapi import Fred
from matplotlib.ticker import FixedFormatter, FixedLocator
from prettytable import PrettyTable

import diy_bbt.providers.utils.spider as spider
import diy_bbt.utils as utils

api_key = os.environ["KEY_FRED"]
fred = Fred(api_key=api_key)

MACRO_MENU = {
    "comdep, cd": "% change commercial bank deposits",
    "cpi": "sticky price cpi less food and energy",
    "cpiuk, cu": "total all items cpi for UK",
    "gdp": "US nominal GDP",
    "gdpr, gr": "US real GDP",
    "gini, g": "US gini index",
    "ginuk, gk": "UK gini index",
    "industry, i": "industries by market cap",
    "israt, is": "total business: inventories to sales ratio",
    "lmen, lm": "labor force participation rate - men",
    "lwmen, lw": "labor force participation rate - women",
    "m2": "M2 money supply",
    "m2vel, 2v": "velocity of M2 money stock",
    "mg30": "US 30-Year fixed rate mortgage average",
    "news, n": "latest headlines",
    "sector, s": "sectors by market cap",
    "sp500": "S&P500",
    "t10y2y, tt": "10-year treasury minus 2-year treasury constant maturity",
    "unrate, ur": "unemployment rate",
    "walcl, wl": "fed total assets: Wednesday level",
}


# Helper functions
def help():
    return utils.help(menu=MACRO_MENU, home=False)


def string():
    return "macro"


def create_table(series_id: str, lim: int):
    data = fred.get_series(series_id)
    table = PrettyTable()
    table.header = False
    table.field_names = ["Date", "Value"]
    count = 0
    for date, value in data.iloc[::-1].items():
        table.add_row([date.strftime("%Y-%m-%d"), utils.format_float(value)])
        count += 1
        if count >= lim:
            break
    return table


def create_plot(series_id, title, xlabel, ylabel):
    data = fred.get_series(series_id)
    df = pd.DataFrame(data).dropna()
    df.index = pd.to_datetime(df.index)
    posix_timestamps = df.index.astype(int) // 10**9
    df.index = posix_timestamps

    plt.style.use("dark_background")
    ax = df.plot(title=title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.get_legend().remove()
    xtick_labels = [
        pd.to_datetime(ts, unit="s").strftime("%Y") for ts in ax.get_xticks()
    ]
    ax.xaxis.set_major_locator(FixedLocator(ax.get_xticks()))
    ax.xaxis.set_major_formatter(FixedFormatter(xtick_labels))
    plt.setp(ax.get_xticklabels(), rotation=45)

    def format_cursor_annotation(sel):
        x_value = pd.to_datetime(sel.target[0], unit="s")
        y_value = sel.target[1]
        sel.annotation.set_text(f"{x_value.strftime('%Y-%m-%d')}\n{y_value:.2f}")

    cursor = mplcursors.cursor(ax)
    cursor.connect("add", format_cursor_annotation)
    plt.show()


# Command functions
def comdep(lim: str = "12", options=()):
    if "-p" in options:
        create_plot(
            "H8B1058NCBCMG",
            "Deposits, All Commercial Banks",
            "Date",
            "Percent Change at Annual Rate",
        )
        return ""
    else:
        table = create_table("H8B1058NCBCMG", int(lim))
        table = utils.green_red_colouring(table, indices=[1])
        return f"{str(table)}"


def cpi(lim: str = "12", options=()):
    if "-p" in options:
        create_plot(
            "CORESTICKM159SFRBATL",
            "Sticky Price Consumer Price Index less Food and Energy",
            "Date",
            "Percent Change from Year Ago",
        )
        return ""
    else:
        table = create_table("CORESTICKM159SFRBATL", int(lim))
        return f"{str(table)}"


def cpiuk(lim: str = "12", options=()):
    if "-p" in options:
        create_plot(
            "CPALTT01GBM659N",
            "Consumer Price Index: Total All Items for the United Kingdom",
            "Date",
            "Growth Rate Same Period Previous Year",
        )
        return ""
    else:
        table = create_table("CPALTT01GBM659N", int(lim))
        return f"{str(table)}"


def fedrate(lim: str = "12", options=()):
    if "-p" in options:
        create_plot("FEDFUNDS", "Federal Funds Effective Rate", "Date", "Percent")
        return ""
    else:
        table = create_table("FEDFUNDS", int(lim))
        return f"{str(table)}"


def gdp(lim: str = "12", options=()):
    if "-p" in options:
        create_plot("GDP", "Nominal GDP", "Date", "Billions USD")
        return ""
    else:
        table = create_table("GDP", int(lim))
        return f"{str(table)}"


def gdpr(lim: str = "12", options=()):
    if "-p" in options:
        create_plot("GDPC1", "Real GDP", "Date", "Billions Chained USD")
        return ""
    else:
        table = create_table("GDPC1", int(lim))
        return f"{str(table)}"


def gini(lim: str = "12", options=()):
    if "-p" in options:
        create_plot("SIPOVGINIUSA", "GINI Index for the United States", "Date", "Index")
        return ""
    else:
        table = create_table("SIPOVGINIUSA", int(lim))
        return f"{str(table)}"


def ginuk(lim: str = "12", options=()):
    if "-p" in options:
        create_plot(
            "SIPOVGINIGBR", "GINI Index for the United Kingdom", "Date", "Index"
        )
        return ""
    else:
        table = create_table("SIPOVGINIGBR", int(lim))
        return f"{str(table)}"


def industry():
    return spider.macro_industry()


def israt(lim: str = "12", options=()):
    if "-p" in options:
        create_plot(
            "ISRATIO", "Total Business: Inventories to Sales Ratio", "Date", "Ratio"
        )
        return ""
    else:
        table = create_table("ISRATIO", int(lim))
        return f"{str(table)}"


def lmen(lim: str = "12", options=()):
    if "-p" in options:
        create_plot(
            "LNS11300001", "Labor Force Participation Rate - Men", "Date", "Percent"
        )
        return ""
    else:
        table = create_table("LNS11300001", int(lim))
        return f"{str(table)}"


def lwmen(lim: str = "12", options=()):
    if "-p" in options:
        create_plot(
            "LNS11300002", "Labor Force Participation Rate - Women", "Date", "Percent"
        )
        return ""
    else:
        table = create_table("LNS11300002", int(lim))
        return f"{str(table)}"


def m2(lim: str = "12", options=()):
    if "-p" in options:
        create_plot("M2", "M2", "Date", "Billions USD")
        return ""
    else:
        table = create_table("M2", int(lim))
        return f"{str(table)}"


def m2vel(lim: str = "12", options=()):
    if "-p" in options:
        create_plot("M2V", "Velocity of M2 Money Stock", "Date", "Ratio")
        return ""
    else:
        table = create_table("M2V", int(lim))
        return f"{str(table)}"


def mg30(lim: str = "12", options=()):
    if "-p" in options:
        create_plot(
            "MORTGAGE30US",
            "30-Year Fixed Rate Mortgage Average in the US",
            "Date",
            "Percent",
        )
        return ""
    else:
        table = create_table("MORTGAGE30US", int(lim))
        return f"{str(table)}"


def news(lim: str = "12"):
    def clean(data: str):
        data = data.replace("UPDATE 1-", "")
        data = data.replace("UPDATE 2-", "")
        data = data.replace("REFILE-", "")
        data = data.replace("UPDATE ", "")
        data = data.replace("\n", "")
        return data

    response = httpx.get("https://www.reuters.com/news/archive/economicNews")
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.find_all("article")
    data = [
        [x.find("h3").text.strip(), x.find("p").text.strip()]
        for x in articles
        if x.find("h3") and x.find("p")
    ]

    table = PrettyTable()
    table.field_names = ["title", "description"]
    count = 0
    for row in data:
        table.add_row([clean(row[0]), clean(row[1])])
        if count > int(int(lim)):
            break
        count += 1

    table._max_width = {"title": 45, "description": 60}
    table.align = "l"

    return f"{str(table)}"


def sector():
    return spider.macro_sector()


def sp500(lim: str = "12", options=()):
    if "-p" in options:
        create_plot("SP500", "S&P500", "Date", "Billions USD")
        return ""
    else:
        table = create_table("SP500", int(lim))
        return f"{str(table)}"


def t10y2y(lim: str = "12", options=()):
    if "-p" in options:
        create_plot(
            "T10Y2Y",
            "10-Year Treasury Constant Maturity Minus 2-Year Treasury Constant Maturity",
            "Date",
            "Percent",
        )
        return ""
    else:
        table = create_table("T10Y2Y", int(lim))
        return f"{str(table)}"


def unrate(lim: str = "12", options=()):
    if "-p" in options:
        create_plot("UNRATE", "Unemplyment Rate", "Date", "Percent")
        return ""
    else:
        table = create_table("UNRATE", int(lim))
        return f"{str(table)}"


def walcl(lim: str = "12", options=()):
    if "-p" in options:
        create_plot(
            "WALCL",
            "Total Assets (Less Eliminations from Consolidation): Wednesday Level",
            "Date",
            "Millions USD",
        )
        return ""
    else:
        table = create_table("WALCL", int(lim))
        return f"{str(table)}"
