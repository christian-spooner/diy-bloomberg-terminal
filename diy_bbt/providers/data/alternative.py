import os

import httpx
from bs4 import BeautifulSoup
from prettytable import PrettyTable

import diy_bbt.utils as utils

api_key = os.environ["KEY_FMP"]

ALTERNATIVE_MENU = {
    "hedge, hf": "hedge funds by aum",
    "priveq, p": "private equity firms by fundraising total",
    "news, n": "headlines by topic: art, hf, ma, pe, re",
    "reit, r": "reits by market cap",
    "vcap, vc": "venture capital firms by aum",
    "zill, z": "zillow research statistics",
}


# Helper functions
def help():
    return utils.help(menu=ALTERNATIVE_MENU, home=False)


def string():
    return "alternative"


# Command functions
def hedge(lim: str = "10"):
    response = httpx.get("https://hedgelists.com/top-250-largest-hedge-funds-2023/")
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("tbody").find_all("tr")
    data = []
    for tr in table:
        td_elements = tr.find_all("td")
        row = []
        for td in td_elements:
            row.append(td.text.strip())

        data.append(row)

    table = PrettyTable()
    table.field_names = [
        "rank",
        "fund",
        "city",
        "aum (millions usd)",
        "strategy",
    ]
    count = 0
    for row in data:
        row[3] = row[3][2:]
        table.add_row(utils.format_string(row))
        count += 1
        if count >= int(lim):
            break

    table.align["fund"] = "l"
    table.align["city"] = "l"
    table.align["strategy"] = "l"

    return f"{str(table)}"


def priveq(lim: str = "10"):
    response = httpx.get("http://breakintope.com/rankings/")
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("tbody").find_all("tr")
    data = []
    for tr in table:
        td_elements = tr.find_all("td")
        row = []
        for td in td_elements:
            row.append(td.text.strip())

        data.append(row)

    table = PrettyTable()
    table.field_names = [
        "rank",
        "fund",
        "L5Y raised ($b)",
        "founded",
        "hq",
        "strategy",
    ]
    count = 0
    for row in data:
        table.add_row(utils.format_string(row[:6]))
        count += 1
        if count >= int(lim):
            break

    table._max_width = {"fund": 48, "hq": 48, "strategy": 48}
    table.align["fund"] = "l"
    table.align["city"] = "l"
    table.align["strategy"] = "l"

    return f"{str(table)}"


def news(topic="hf", lim: str = "12"):
    topic_map = {
        "art": "the-art-market",
        "hf": "hedge-funds",
        "ma": "mergers-acquisitions",
        "pe": "private-equity",
        "re": "property-sector",
    }
    topic = topic_map[topic]
    response = httpx.get(f"https://www.ft.com/{topic}")
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.find(
        "ul", class_="o-teaser-collection__list js-stream-list"
    ).find_all("li")
    data = []
    for x in articles:
        try:
            title = (
                x.find("div", class_="o-teaser__heading")
                .text.replace("Premium\xa0content", "")
                .strip()
            )
            description = x.find("p").text.strip()
            data.append([title, description])
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


def reit(lim: str = "20"):
    response = httpx.get(
        "https://companiesmarketcap.com/reit/largest-reits-by-market-cap/"
    )

    soup = BeautifulSoup(response.content, "html.parser")
    td_elements = soup.find("tbody").find_all("td")
    data = []
    row: list[str] = []
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
    count = 0
    for row in data:
        table.add_row(utils.format_string(row))
        count += 1
        if count >= int(lim):
            break

    table.align["name"] = "l"
    table.del_column("today")
    table.del_column("price 30d")

    return f"{str(table)}"


def vcap(lim: str = "10"):
    response = httpx.get(
        "https://www.swfinstitute.org/fund-manager-rankings/venture-capital-firm"
    )
    soup = BeautifulSoup(response.content, "html.parser")
    rows = soup.find("tbody").find_all("tr")
    data = []
    for x in rows:
        content = x.find_all("td")
        data.append([x.text.strip() for x in content])

    table = PrettyTable()
    table.field_names = ["rank", "name", "aum (millions usd)", "type", "region"]
    count = 0
    for row in data:
        table.add_row(row)
        count += 1
        if count >= int(lim):
            break

    table.align = "l"

    return f"{str(table)}"


def zill():
    response = httpx.get("https://www.zillow.com/research/")
    soup = BeautifulSoup(response.content, "html.parser")
    rows = soup.find("div", class_="goldberg-wysiwyg").find_all("p")
    data = []
    for i in range(0, len(rows), 2):
        data.append(
            [
                rows[i].small.next_sibling.next_sibling.strip().lower(),
                rows[i + 1].text.strip(),
            ]
        )

    table = PrettyTable()
    for row in data:
        table.add_row(row)

    table.align = "l"
    table.header = False

    return f"{str(table)}"
