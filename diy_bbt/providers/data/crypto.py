import re
from datetime import datetime

import colorama
import httpx
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable

import diy_bbt.utils as utils

# api_key = os.environ["KEY_COIN_GECKO"]

CRYPTO_MENU = {
    "airdrop, a": "airdroppable protocols",
    "bridges, br": "bridges by volume",
    "cxtran, c": "cex transparency",
    "deglob, d": "global defi data",
    "exchanges, e": "available exchanges",
    "hacks, hk": "recent hackings",
    "mcap, mc": "cryptocurrencies by market cap",
    "mperc, mp": "cryptocurrencies by market cap %",
    "news, n": "latest news by topic",
    "nft": "top nft collections",
    "price, p": "recent price history",
    "quote, q": "latest quote(s)",
    "stables, s": "stablcoins by market cap",
    "treasury, ts": "public company crypto holdings",
    "trending, tn": "trending tokens",
    "tvl": "tvl rankings",
    "volume, v": "24h volume",
    "yields, y": "yield rankings",
}


# Helper functions
def help():
    return utils.help(menu=CRYPTO_MENU, home=False)


def string():
    return "crypto"


def find_token(token):
    token = token.lower()
    match token:
        case "btc":
            return "bitcoin"
        case "eth":
            return "ethereum"
        case "sol":
            return "solana"
        case _:
            return token


def format_desc(description):
    result = description.replace("\r", "").replace("\n", "")
    if len(result) > 360:
        result = result[:360] + "..."
    return result


# Command functions
def airdrop():
    response = httpx.get("https://defillama.com/airdrops")
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
        "name",
        "category",
        "tvl",
        "total money raised",
        "listed at",
        "1d change",
        "7d change",
        "1m change",
    ]
    for row in data:
        if len(row) > 1:
            row[0] = re.sub(r"^\d+", "", row[0])
            table.add_row(utils.format_string(row))

    table.align["name"] = "l"
    table.align["category"] = "l"
    table = utils.green_red_colouring(table, indices=[5, 6])
    table.del_column("total money raised")
    table.del_column("1m change")

    return f"{str(table)}"


def bridges():
    response = httpx.get("https://defillama.com/bridges")
    soup = BeautifulSoup(response.content, "html.parser")
    tr_elements = soup.find("tbody").find_all("tr")
    data = []
    for tr in tr_elements:
        td_elements = tr.find_all("td")
        row = []
        for i, td in enumerate(td_elements):
            if i == 0:
                row.append(td.find("a").text.strip())
            else:
                row.append(td.text.strip())
        data.append(row)

    table = PrettyTable()
    table.field_names = [
        "name",
        "xxx",
        "1d change",
        "24h volume",
        "7d volume",
        "1m volume",
        "24h # of txns",
    ]
    for row in data[:12]:
        table.add_row(row)

    table.align["name"] = "l"
    table.del_column("xxx")

    def color_value(val: str):
        if val.startswith("+"):
            return colorama.Fore.GREEN + val + colorama.Style.RESET_ALL
        elif val.startswith("-"):
            return colorama.Fore.RED + val + colorama.Style.RESET_ALL
        return val

    for row in table.rows:
        row[1] = color_value(row[1])

    return f"{str(table)}"


def cxtran():
    response = httpx.get("https://defillama.com/cexs")
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
        "name",
        "assets",
        "clean assets",
        "24h inflows",
        "7d inflows",
        "1m inflows",
        "auditor",
        "last audit data",
        "spot volume",
        "24h open interest",
        "avg leverage",
    ]
    for row in data:
        if len(row) == 11:
            row[0] = re.sub(r"^\d+", "", row[0])
            table.add_row(utils.format_string(row))

    table.align["name"] = "l"
    table.del_column("auditor")
    table.del_column("last audit data")

    def color_value(val: str):
        if val.startswith("+"):
            return colorama.Fore.GREEN + val + colorama.Style.RESET_ALL
        elif val.startswith("-"):
            return colorama.Fore.RED + val + colorama.Style.RESET_ALL
        return val

    for row in table.rows:
        row[3:5] = [color_value(row[3]), color_value(row[4]), color_value(row[5])]

    return f"{str(table)}"


def deglob():
    data = requests.get(
        "https://api.coingecko.com/api/v3/global/decentralized_finance_defi"
    ).json()["data"]
    table = PrettyTable()

    for key in data:
        try:
            value = float(data[key])
        except Exception:
            value = data[key]
        table.add_row([utils.format_string(key), utils.format_float(value, 4)])

    table.align["Field 1"] = "l"
    table.header = False

    return f"{str(table)}"


def exchanges():
    data = requests.get("https://api.coingecko.com/api/v3/exchanges").json()
    table = PrettyTable()
    table.field_names = [
        "id",
        "trust rank",
        "24h trade volume btc",
        "description",
    ]

    for item in data:
        table.add_row(
            [
                item["id"],
                item["trust_score_rank"],
                utils.format_float(item["trade_volume_24h_btc"], 4),
                format_desc(str(item["description"])),
            ]
        )

    table._max_width = {"description": 90}
    table.align["description"] = "l"

    return f"{str(table)}"


def hacks():
    response = httpx.get("https://defillama.com/hacks")
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
        "name",
        "date",
        "amount lost",
        "chains",
        "classification",
        "technique",
        "link",
    ]
    for row in data:
        if len(row) == 7:
            table.add_row(utils.format_string(row))

    table.align = "l"
    table.del_column("chains")
    table.del_column("link")

    return f"{str(table)}"


def mcap():
    response = httpx.get("https://coinmarketcap.com/")
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("tbody")
    tr_elements = table.find_all("tr")
    data = []
    for tr in tr_elements:
        row = []
        for i, td in enumerate(tr.find_all("td")):
            content = td.text.strip()

            match i:
                case 2:
                    el = td.find("p")
                    if el is not None:
                        content = el.text.strip()
                case i if i in (4, 5, 6):
                    el = td.find("span").find("span")
                    if (
                        el is not None
                        and "down" in el.get("class")[0]
                        and content != "0.00"
                    ):
                        content = "-" + content
                case 7:
                    el = td.find("p").find("span")
                    if el is not None:
                        content = el.text.strip()
                case 8:
                    el = td.find("p")
                    if el is not None:
                        content = el.text.strip()
                case _:
                    pass

            if content:
                row.append(content)
        data.append(row)

    table = PrettyTable()
    table.field_names = [
        "rank",
        "name",
        "price",
        "1h %",
        "24h %",
        "7d %",
        "market cap",
        "24h volume",
        "supply",
    ]
    for row in data:
        if len(row) >= 9:
            table.add_row(utils.format_string(row[:9]))

    table.align["name"] = "l"
    table = utils.green_red_colouring(table, indices=[3, 4, 5])

    return f"{str(table)}"


def mperc():
    data = requests.get("https://api.coingecko.com/api/v3/global").json()["data"][
        "market_cap_percentage"
    ]
    table = PrettyTable()
    table.field_names = [
        "token",
        "market cap %",
    ]

    for key in data:
        table.add_row([key, utils.format_float(data[key])])

    return f"{str(table)}"


def news(topic="defi"):
    response = httpx.get(f"https://cointelegraph.com/tags/{topic.lower()}")
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.find_all("span", class_="post-card-inline__title")
    det = soup.find_all("p", class_="post-card-inline__text")
    pub = soup.find_all("time", class_="post-card-inline__date")
    table = PrettyTable()
    table.field_names = ["title", "detail", "published"]
    count = 0
    for i in range(len(title)):
        table.add_row([title[i].text.strip(), det[i].text.strip(), pub[i].text.strip()])
        if count > 24:
            break
        count += 1

    table._max_width = {"title": 45, "detail": 45}
    table.align = "l"

    return f"{str(table)}"


def nft():
    response = httpx.get("https://defillama.com/nfts")
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
        "name",
        "floor price",
        "1d change",
        "7d change",
        "volume 1d",
        "volume 7d",
        "sales 1d",
        "total supply",
        "on sale",
    ]
    for row in data:
        if len(row) == 9:
            table.add_row(utils.format_string(row))

    table.align["name"] = "l"
    table = utils.green_red_colouring(table, indices=[2, 3])

    return f"{str(table)}"


def price(ticker="bitcoin", lim_str: str = "12"):
    lim = int(lim_str)
    data = requests.get(
        f"https://api.coingecko.com/api/v3/coins/{ticker}"
        + f"/market_chart?vs_currency=usd&days={lim + 1}&interval=daily"
    ).json()
    table = PrettyTable()
    table.field_names = ["date", "price", "% change", "volume", "market cap"]
    for i in range(lim):
        row = [
            str(datetime.fromtimestamp(data["prices"][-i - 1][0] / 1000).date()),
            utils.format_float(data["prices"][-i - 1][1]),
            utils.format_float(
                (100 * data["prices"][-i - 1][1] / data["prices"][-i - 2][1]) - 100
            ),
            utils.format_int(data["total_volumes"][-i - 1][1]),
            utils.format_int(data["market_caps"][-i - 1][1]),
        ]
        table.add_row(row)

    table = utils.green_red_colouring(table, indices=[2])

    return f"{str(table)}"


def quote(*tokens):
    token_csv = ""
    if tokens:
        for token in tokens:
            token_csv += find_token(token) + ","
    else:
        token_csv = "bitcoin"
    data = requests.get(
        f"https://api.coingecko.com/api/v3/simple/price?ids={token_csv}&vs_currencies=usd"
    ).json()

    table = PrettyTable()
    table.field_names = ["token", "price/usd"]
    for key in data:
        table.add_row([key, utils.format_float(data[key]["usd"])])

    table.header = False

    return f"{str(table)}"


def stables():
    response = httpx.get("https://defillama.com/stablecoins")
    soup = BeautifulSoup(response.content, "html.parser")
    tr_elements = soup.find("tbody").find_all("tr")
    data = []
    for tr in tr_elements:
        td_elements = tr.find_all("td")
        row = []
        for i, td in enumerate(td_elements):
            try:
                if i == 0:
                    row.append(td.find("a").text.strip())
                else:
                    row.append(td.text.strip())
            except Exception:
                row.append("")
        data.append(row)

    table = PrettyTable()
    table.field_names = [
        "name",
        "xxx",
        "% off peg",
        "1m % off peg",
        "price",
        "1d change",
        "7d change",
        "1m change",
        "market cap",
    ]
    for row in data[:12]:
        table.add_row(row)

    table.align["name"] = "l"
    table.del_column("xxx")

    def color_value(val: str):
        if val.startswith("+"):
            return colorama.Fore.GREEN + val + colorama.Style.RESET_ALL
        elif val.startswith("-"):
            return colorama.Fore.RED + val + colorama.Style.RESET_ALL
        return val

    for row in table.rows:
        row[1] = color_value(row[1])
        row[2] = color_value(row[2])
        row[4] = color_value(row[4])
        row[5] = color_value(row[5])
        row[6] = color_value(row[6])

    return f"{str(table)}"


def treasury(token="bitcoin"):
    token = find_token(token)
    data = requests.get(
        f"https://api.coingecko.com/api/v3/companies/public_treasury/{token}"
    ).json()["companies"]
    table = PrettyTable()
    table.field_names = utils.format_string(list(data[0].keys()))

    for item in data:
        table.add_row(
            [utils.format_string(utils.format_float(x)) for x in list(item.values())]
        )

    return f"{str(table)}"


def trending():
    data = requests.get("https://api.coingecko.com/api/v3/search/trending").json()[
        "coins"
    ]
    table = PrettyTable()
    table.field_names = utils.format_string(list(data[0]["item"].keys()))
    table.field_names.remove("thumb")
    table.field_names.remove("small")
    table.field_names.remove("large")

    for item in data:
        row = [utils.format_float(x, 8) for x in list(item["item"].values())]
        row = row[:5] + row[8:]
        table.add_row(row)

    table.del_column("score")

    return f"{str(table)}"


def tvl():
    response = httpx.get("https://defillama.com/")
    soup = BeautifulSoup(response.content, "html.parser")
    tr_elements = soup.find("tbody").find_all("tr")
    data = []
    for tr in tr_elements:
        td_elements = tr.find_all("td")
        if len(td_elements) == 7:
            order = [0, 1, 3, 4, 5, 2, 6]
            td_elements = [td_elements[x] for x in order]
            row = []
            for i, td in enumerate(td_elements):
                if i == 0:
                    row.append(td.find("a").text.strip())
                else:
                    row.append(td.text.strip())
            data.append(row)

    table = PrettyTable()
    table.field_names = [
        "name",
        "category",
        "1d change",
        "7d change",
        "1m change",
        "tvl",
        "mcap/tvl",
    ]
    for row in data:
        table.add_row(utils.format_string(row))

    table.align["name"] = "l"
    table.align["category"] = "l"
    table = utils.green_red_colouring(table, indices=[2, 3, 4])

    return f"{str(table)}"


def volume():
    data = requests.get("https://api.coingecko.com/api/v3/global").json()["data"][
        "total_volume"
    ]
    data = {k: data[k] for k in sorted(data)}
    table = PrettyTable()
    table.field_names = [
        "token",
        "24h volume",
    ]

    for key in data:
        table.add_row([key, utils.format_float(data[key])])

    return f"{str(table)}"


def yields():
    response = httpx.get("https://defillama.com/yields")
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
        "pool",
        "project",
        "chain",
        "tvl",
        "apy",
        "base apy",
        "reward apy",
        "30d avg apy",
        "30d apy chart",
    ]
    for row in data:
        row[0] = re.sub(r"^\d+", "", row[0])
        if len(row) == 9:
            row[6] = row[6].replace("+", "")
            table.add_row(utils.format_string(row))

    table.align = "l"
    table.del_column("chain")
    table.del_column("30d apy chart")

    return f"{str(table)}"
