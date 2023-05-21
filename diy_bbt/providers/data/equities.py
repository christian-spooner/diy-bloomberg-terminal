import csv
import os
import sys
import time

import httpx
import pandas as pd
import requests
import yahooquery as yq
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from prettytable import PrettyTable

import diy_bbt.utils as utils

api_key = os.environ["KEY_TWELVE_DATA"]

EQUITIES_MENU = {
    "certs, c": "major certificates",
    "daygain, dg": "top gaining stocks today",
    "daylose, dl": "top losing stocks today",
    "description, d": "business description",
    "etf": "top etfs by assets",
    "etfp, ep": "top etfs by performance",
    "exchanges, ex": "available exchanges",
    "indices, i": "major indices",
    "indfut, if": "indices futures",
    "mcap, m": "largest companies by market cap",
    "mutf, mt": "top mutual funds by assets",
    "mutp, mp": "top mutual funds by performance",
    "news, n": "latest headlines",
    "price, p": "recent price history",
    "quotemon, qm": "live quote monitor",
    "quote, q": "latest quote(s)",
    "summary, s": "summary details",
    "symbol, sm": "fuzzy find symbol or company name",
    "trending, t": "trending tickers",
}


# Helper functions
def help():
    return utils.help(menu=EQUITIES_MENU, home=False)


def string():
    return "equities"


def drawScreen(tickers, columnwidth, rows):
    for i in range(len(tickers)):
        k = i // rows
        sys.stdout.write("\033[K")
        sys.stdout.write(
            "\033[33m" + tickers[i] + "-" * (columnwidth - len(tickers[i])) + "\033[0m"
        )
        sys.stdout.write("\033[{};{}H".format(i % rows + 2, k * columnwidth + 1))
    sys.stdout.flush()


# Command functions
def certs():
    response = httpx.get("https://www.investing.com/certificates/major-certificates")
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("tbody")
    tr_elements = table.find_all("tr")
    data = []
    for tr in tr_elements:
        td_elements = tr.find_all("td")
        row = []
        for td in td_elements[1:7]:
            row.append(td.text.strip())
        data.append(row)

    table = PrettyTable()
    table.field_names = [
        "name",
        "symbol",
        "last",
        "% change",
        "volume",
        "time",
    ]
    for row in data:
        table.add_row(utils.format_string(row))

    table.align["name"] = "l"
    table.align["symbol"] = "l"
    table = utils.green_red_colouring(table, indices=[3])

    return f"{str(table)}"


def daygain(lim: str = "12"):
    data = yq.Screener().get_screeners(["day_gainers"], int(lim))["day_gainers"][
        "quotes"
    ]
    table = PrettyTable()
    table.field_names = ["name", "% change", "volume"]
    for item in data:
        table.add_row(
            [
                utils.format_string(item["shortName"]),
                utils.format_float(
                    100 * item["regularMarketChange"] / item["regularMarketPrice"]
                ),
                utils.format_float(item["regularMarketVolume"]),
            ]
        )

    table = utils.green_red_colouring(table, indices=[1])
    table.align["name"] = "l"

    return f"{str(table)}"


def daylose(lim: str = "12"):
    data = yq.Screener().get_screeners(["day_losers"], int(lim))["day_losers"]["quotes"]
    table = PrettyTable()
    table.field_names = ["name", "% change", "volume"]
    for item in data:
        table.add_row(
            [
                utils.format_string(item["shortName"]),
                utils.format_float(
                    100 * item["regularMarketChange"] / item["regularMarketPrice"]
                ),
                utils.format_float(item["regularMarketVolume"]),
            ]
        )

    table = utils.green_red_colouring(table, indices=[1])
    table.align["name"] = "l"

    return f"{str(table)}"


def description(ticker="MSFT"):
    data = yq.Ticker(ticker).asset_profile[ticker]["longBusinessSummary"]
    table = PrettyTable()
    table.add_row([data])

    table.field_names = ["A"]
    table._max_width = {"A": 90}
    table.align["A"] = "l"
    table.header = False

    return f"{str(table)}"


def etf(lim: str = "12"):
    response = httpx.get("https://etfdb.com/compare/market-cap/")
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("tbody")
    tr_elements = table.find_all("tr")
    data = []
    for tr in tr_elements:
        td_elements = tr.find_all("td")
        row = []
        for td in td_elements:
            row.append(td.text.strip())
        data.append(row)

    table = PrettyTable()
    table.field_names = [
        "symbol",
        "name",
        "aum",
        "avg daily volume",
    ]
    for i, row in enumerate(data):
        if i >= int(lim):
            break
        table.add_row(utils.format_string(row))

    table.align["name"] = "l"

    return f"{str(table)}"


def etfp(lim: str = "12"):
    data = yq.Screener().get_screeners(["top_performing_etfs"], int(lim))[
        "top_performing_etfs"
    ]["quotes"]
    table = PrettyTable()
    table.field_names = ["ticker", "name", "price", "% change", "ytd return"]
    for item in data:
        ytdReturn: str | float
        if "ytdReturn" in item:
            ytdReturn = float(item["ytdReturn"])
        else:
            ytdReturn = "n/a"
        table.add_row(
            [
                utils.format_string(item["symbol"]),
                utils.format_string(item["shortName"]),
                utils.format_float(item.get("regularMarketPrice", "n/a")),
                utils.format_float(item.get("regularMarketChangePercent", "n/a")),
                utils.format_float(ytdReturn),
            ]
        )

    table = utils.green_red_colouring(table, indices=[3, 4])
    table = table.get_string(sortby="ytd return", reversesort=True)  # type: ignore

    table.align["name"] = "l"

    return f"{str(table)}"


def exchanges():
    data = yq.get_exchanges()
    table = PrettyTable()
    table.field_names = data.columns
    for row in data.itertuples():
        table.add_row(row[1:])
    return f"{str(table)}"


def indices():
    response = httpx.get("https://www.investing.com/indices/major-indices")
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("tbody", class_="datatable_body__cs8vJ")
    tr_elements = table.find_all("tr")
    data = []
    for tr in tr_elements:
        td_elements = tr.find_all("td")
        row = []
        for td in td_elements:
            if len(td) > 1:
                temp = []
                for el in td.children:
                    temp.append(el.text.strip())
                row.extend(temp)
            else:
                row.append(td.text.strip())
        data.append(row)

    table = PrettyTable()
    table.field_names = [
        "index",
        "last",
        "high",
        "low",
        "change",
        "% change",
        "time",
        "exchange",
    ]
    for row in data:
        row = row[1:9]
        row[0] = row[0].replace("derived", "")
        table.add_row(utils.format_string(row))

    table.align["index"] = "l"
    table.align["exchange"] = "l"
    table = utils.green_red_colouring(table, indices=[4, 5])

    return f"{str(table)}"


def indfut():
    response = httpx.get("https://www.investing.com/indices/indices-futures")
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("tbody", class_="datatable_body__cs8vJ")
    tr_elements = table.find_all("tr")
    data = []
    for tr in tr_elements:
        td_elements = tr.find_all("td")
        row = []
        for td in td_elements:
            if td.text:
                text = td.text.strip()
            else:
                text = td.text
            row.append(text.replace("derived", "").replace("Ex.", ""))

        data.append(row)

    table = PrettyTable()
    table.field_names = [
        "index",
        "month",
        "last",
        "high",
        "low",
        "change",
        "% change",
        "time",
    ]
    for row in data:
        row = row[1:9]
        table.add_row(utils.format_string(row))

    table.align["index"] = "l"
    table.align["exchange"] = "l"
    table = utils.green_red_colouring(table, indices=[5, 6])

    return f"{str(table)}"


def mcap(*country):
    if country:
        country = "-".join(country)
        if country == "united-kingdom" or country == "uk":
            response = httpx.get(
                "https://companiesmarketcap.com/united-kingdom/largest-companies-in-the-uk-by-market-cap/"
            )
        else:
            response = httpx.get(
                f"https://companiesmarketcap.com/{country}/largest-companies-in-{country}-by-market-cap/"
            )
    else:
        response = httpx.get("https://companiesmarketcap.com/")

    soup = BeautifulSoup(response.content, "html.parser")
    td_elements = soup.find("tbody").find_all("td")
    data = []
    row = []
    for i, td in enumerate(td_elements):
        if i % 7 == 0 and i > 0:
            data.append(row)
            row = []
            row.append(td.text.strip())
        elif i % 7 == 1:
            row.append(td.find("div", class_="company-name").text.strip())
        elif i % 7 == 6:
            row.append(td.find("span").text.strip())
        else:
            row.append(td.text.strip())

    table = PrettyTable()
    table.field_names = [
        "rank",
        "name",
        "market cap",
        "price",
        "today",
        "price 30d",
        "country",
    ]
    for row in data:
        table.add_row(utils.format_string(row))

    table.align["name"] = "l"
    table.del_column("today")
    table.del_column("price 30d")

    return f"{str(table)}"


def mutf(lim: str = "12"):
    response = httpx.get("https://www.marketwatch.com/tools/top-25-mutual-funds")
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("tbody")
    tr_elements = table.find_all("tr")
    data = []
    for tr in tr_elements:
        td_elements = tr.find_all("td")
        row = []
        for td in td_elements:
            row.append(td.text.strip())
        data.append(row)

    table = PrettyTable()
    table.field_names = [
        "rank",
        "symbol",
        "name",
    ]
    for i, row in enumerate(data):
        if i >= int(lim):
            break
        table.add_row(utils.format_string(row))

    table.align["symbol"] = "l"
    table.align["name"] = "l"

    return f"{str(table)}"


def mutp(lim: str = "12"):
    data = yq.Screener().get_screeners(["top_mutual_funds"], int(lim))[
        "top_mutual_funds"
    ]["quotes"]
    table = PrettyTable()
    table.field_names = ["ticker", "name", "price", "% change", "ytd return"]
    for item in data:
        ytdReturn: str | float
        if "ytdReturn" in item:
            ytdReturn = float(item["ytdReturn"])
        else:
            ytdReturn = "n/a"
        table.add_row(
            [
                utils.format_string(item["symbol"]),
                utils.format_string(item["shortName"]),
                utils.format_float(item.get("regularMarketPrice", "n/a")),
                utils.format_float(item.get("regularMarketChangePercent", "n/a")),
                utils.format_float(ytdReturn),
            ]
        )

    table.align["name"] = "l"
    table = utils.green_red_colouring(table, indices=[3, 4])
    table = table.get_string(sortby="% change", reversesort=True)  # type: ignore

    return f"{str(table)}"


def news(ticker="MSFT"):
    response = httpx.get(
        f"https://www.marketwatch.com/investing/stock/{ticker.lower()}?mod=search_symbol"
    )
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.find("div", class_="collection__elements j-scrollElement").find_all(
        "div", class_="article__content"
    )
    data = []
    for element in content:
        if (h3 := element.find("h3")) is not None:
            data.append(h3.find("a").text.strip())

    table = PrettyTable()
    for item in data:
        table.add_row([item])

    table.align = "l"
    table.header = False

    return f"{str(table)}"


def price(ticker="MSFT", lim: str = "12"):
    api_url = f"https://api.twelvedata.com/time_series?symbol={ticker}&interval=1day&outputsize=5000&apikey={api_key}"
    raw_df = requests.get(api_url).json()
    df = pd.DataFrame(raw_df["values"]).set_index("datetime").astype(float)
    table = PrettyTable()
    table.field_names = ["date"] + utils.format_string(list(df.keys()))
    count = 0
    for row in df.itertuples():
        table.add_row(
            [utils.format_float(x) for x in row[:5]] + [utils.format_int(row[5])]
        )
        count += 1
        if count > int(lim):
            break

    return f"{str(table)}"


def quote(*tickers):
    tickers = tickers if tickers else ("MSFT", "AAPL")
    quotes = [
        yq.Ticker(ticker).quotes[ticker.upper()]["regularMarketPrice"]
        for ticker in tickers
    ]
    table = PrettyTable()
    for i, ticker in enumerate(tickers):
        table.add_row([ticker.lower(), quotes[i]])

    table.header = False

    return f"{str(table)}"


def quotemonitor(*tickers):
    os.system("cls" if os.name == "nt" else "clear")
    columnwidth = 20
    rows = 30
    drawScreen(tickers, columnwidth, rows)

    try:
        while True:
            for ticker in tickers:
                res = requests.get(
                    "https://generic709.herokuapp.com/stockc/{}".format(ticker)
                )
                quote = res.json()
                if not quote:
                    continue
                xposition = 10 + (tickers.index(ticker) // rows) * columnwidth
                yposition = tickers.index(ticker) % rows + 1
                sys.stdout.write("\033[{};{}H".format(yposition, xposition))
                sys.stdout.write("\033[37m" + "{:.2f}".format(quote["price"]))
                sys.stdout.flush()
                time.sleep(0.5)
    except KeyboardInterrupt:
        return "CLEAR"


def summary(ticker="MSFT"):
    data = yq.Ticker(ticker.lower()).summary_detail[ticker.lower()]
    table = PrettyTable()
    for key, value in data.items():
        table.add_row([utils.format_string(key), utils.format_float(value)])

    table.align["Field 1"] = "l"
    table.header = False

    return f"{str(table)}"


def symbol(*text):
    def find_closest_match(input, symbol_table):
        best_match_score = 0
        best_match = None
        for row in symbol_table:
            company_name = row[1]
            match_score = fuzz.ratio(input.lower(), company_name.lower())
            if match_score > best_match_score:
                best_match_score = match_score
                best_match = row

            symbol = row[0]
            match_score = fuzz.ratio(input.lower(), symbol.lower())
            if match_score > best_match_score:
                best_match_score = match_score
                best_match = row
        return best_match

    name = " ".join(text)
    symbol_table = []
    with open("diy_bbt/storage/files/symbol_table.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0].startswith("#"):
                continue
            symbol_table.append(row)

    best_match = find_closest_match(name, symbol_table)
    if best_match is not None:
        symbol = best_match[0]
        company_name = best_match[1]

    table = PrettyTable()
    table.add_row([symbol, company_name])
    table.header = False

    return f"{str(table)}"


def trending():
    response = httpx.get("https://finance.yahoo.com/trending-tickers")
    soup = BeautifulSoup(response.content, "html.parser")
    tr_elements = soup.find("tbody").find_all("tr")
    data = []
    for tr in tr_elements:
        td_elements = tr.find_all("td")
        row = []
        for td in td_elements:
            row.append(td.text.strip())
        data.append(row)

    table = PrettyTable()
    table.field_names = [
        "ticker",
        "name",
        "last",
        "time",
        "change",
        "% change",
        "volume",
        "market cap",
    ]
    for row in data:
        table.add_row(utils.format_string(row[:8]))

    table.del_column("name")
    table.del_column("time")
    table = utils.green_red_colouring(table, indices=[2, 3])

    return f"{str(table)}"
