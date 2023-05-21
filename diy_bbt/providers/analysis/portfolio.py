import functools
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import seaborn as sns
from prettytable import PrettyTable

import diy_bbt.utils as utils

api_key = os.environ["KEY_TWELVE_DATA"]

PORTFOLIO_MENU = {
    "corr, c": "historical asset price correlation",
    "meancorr, mc": "mean absolute correlation",
    "return, r": "historical return",
    "sumcorr, sc": "summed absolute correlations",
    "variance, v": "historical variance",
}


# Helper functions
def help():
    return utils.help(menu=PORTFOLIO_MENU, home=False)


def string():
    return "portfolio"


def add_index(table, fields):
    table._field_names.insert(0, "")
    table._align[""] = table.align
    table._valign[""] = table.valign
    for i, row in enumerate(table._rows):
        row.insert(0, fields[i])
    return table


@functools.lru_cache()
def get_historical_data(symbol, start_date=None, end_date=None):
    api_url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=1day&outputsize=5000&apikey={api_key}"
    raw_df = requests.get(api_url).json()
    df = pd.DataFrame(raw_df["values"]).iloc[::-1].set_index("datetime").astype(float)
    if start_date is not None:
        df = df[df.index >= start_date]
    if end_date is not None:
        df = df[df.index <= end_date]
    df.index = pd.to_datetime(df.index)
    return df


# controllers
def corr(*tickers, options=()):
    if len(tickers) == 2:
        ticker1 = tickers[0]
        ticker2 = tickers[1]
        ticker1_data = get_historical_data(ticker1)
        ticker2_data = get_historical_data(ticker2)
        rets_df = pd.DataFrame(
            {
                ticker1: ticker1_data["close"] / ticker1_data["close"].iloc[0],
                ticker2: ticker2_data["close"] / ticker2_data["close"].iloc[0],
            }
        ).dropna()
        table = PrettyTable()
        table.add_row([utils.format_float(rets_df.corr().iloc[0][1], i=4)])
        table.header = False
        return f"{str(table)}"
    else:
        tickers_data = []
        for ticker in tickers:
            ticker_data = get_historical_data(ticker)
            tickers_data.append(ticker_data)
        tickers_close = pd.DataFrame()
        for i in range(len(tickers)):
            close_prices = tickers_data[i]["close"] / tickers_data[i]["close"].iloc[0]
            tickers_close[tickers[i]] = close_prices
        tickers_close = tickers_close.dropna()
        data = tickers_close.corr()
        if "-p" in options:
            plt.style.use("default")
            sns.heatmap(data, annot=True, linewidths=0.5)
            plt.show()
            return ""
        table = PrettyTable()
        table.field_names = data.columns
        for row in data.iterrows():
            formatted_row = [utils.format_float(x, i=4) for x in row[1]]
            table.add_row(formatted_row)
        table = add_index(table, data.columns)
        return f"{str(table)}"


def meancorr(*tickers):
    if len(tickers) == 2:
        return f"{str(abs(float(corr(*tickers))))}"
    else:
        tickers_data = []
        for ticker in tickers:
            ticker_data = get_historical_data(ticker)
            tickers_data.append(ticker_data)
        tickers_close = pd.DataFrame()
        for i in range(len(tickers)):
            close_prices = tickers_data[i]["close"] / tickers_data[i]["close"].iloc[0]
            tickers_close[tickers[i]] = close_prices
        tickers_close = tickers_close.dropna()
        df = tickers_close.corr()
        df = pd.DataFrame(np.tril(df.values), index=df.index, columns=df.columns)
        df = df.where(np.tril(np.ones(df.shape), k=-1).astype(bool))
        count = df.count().sum()
        sum = df.abs().sum().sum()
        return f"{utils.format_float(sum / count, i=4)}"


def sumcorr(*tickers):
    if len(tickers) == 2:
        return f"{str(abs(float(corr(*tickers))))}"
    else:
        tickers_data = []
        for ticker in tickers:
            ticker_data = get_historical_data(ticker)
            tickers_data.append(ticker_data)
        tickers_close = pd.DataFrame()
        for i in range(len(tickers)):
            close_prices = tickers_data[i]["close"] / tickers_data[i]["close"].iloc[0]
            tickers_close[tickers[i]] = close_prices
        tickers_close = tickers_close.dropna()
        df = tickers_close.corr()
        data = df.abs().sum() - 1
        table = PrettyTable()
        table.field_names = data.index.values
        vals = []
        for x in data:
            vals.append(utils.format_float(x, i=4))
        table.add_row(vals)
        return f"{str(table)}"


def returns(*args):
    n = len(args) // 2
    tickers = args[:n]
    weights = (
        pd.DataFrame([float(x) for x in args[n:]], index=tickers, columns=["weight"])
        .to_numpy()
        .T
    )
    tickers_data = []
    for ticker in tickers:
        ticker_data = get_historical_data(ticker)
        tickers_data.append(ticker_data)
    tickers_close = pd.DataFrame()
    for i in range(len(tickers)):
        close_prices = tickers_data[i]["close"] / tickers_data[i]["close"].iloc[0]
        tickers_close[tickers[i]] = close_prices
    tickers_rets = tickers_close.dropna().tail(1)
    data = np.dot(weights, tickers_rets.T)

    table = PrettyTable()
    table.add_row([utils.format_float(float(data))])
    table.header = False

    return f"{str(table)}"


def variance(*args):
    n = len(args) // 2
    tickers = args[:n]
    weights = (
        pd.DataFrame([float(x) for x in args[n:]], index=tickers, columns=["weight"])
        .to_numpy()
        .T
    )
    tickers_data = []
    for ticker in tickers:
        ticker_data = get_historical_data(ticker)
        tickers_data.append(ticker_data)
    tickers_close = pd.DataFrame()
    for i in range(len(tickers)):
        close_prices = tickers_data[i]["close"] / tickers_data[i]["close"].iloc[0]
        tickers_close[tickers[i]] = close_prices
    tickers_close = tickers_close.dropna()
    covariance_matrix = np.cov(tickers_close.T)
    data = np.dot(weights, np.dot(covariance_matrix, weights.T))

    table = PrettyTable()
    table.add_row([utils.format_float(float(data))])
    table.header = False

    return f"{str(table)}"
