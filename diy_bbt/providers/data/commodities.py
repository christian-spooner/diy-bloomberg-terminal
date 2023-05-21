import httpx
from bs4 import BeautifulSoup
from prettytable import PrettyTable

import diy_bbt.providers.utils.spider as spider
import diy_bbt.utils as utils

COMMODITIES_MENU = {
    "cush, c": "cushing, oklahoma suppply levels",
    "elec, e": "electricity prices",
    "energy, en": "energy futures prices",
    "futures, f": "major commodity futures prices",
    "grains, g": "grains futures prices",
    "indices, i": "major indices",
    "meats, m": "meats futures prices",
    "metals, mt": "metals futures prices",
    "news, n": "latest headlines",
    "quote, q": "latest quote(s)",
    "softs, s": "softs futures prices",
    "symbols, sm": "list available commodity symbols",
}


# Helper functions
def help():
    return utils.help(menu=COMMODITIES_MENU, home=False)


def string():
    return "commodities"


def commodity_table(uri):
    response = httpx.get(f"https://www.investing.com/commodities/{uri}")
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", id="cross_rate_1")
    tr_elements = table.find_all("tbody")[0].find_all("tr")
    data = []
    for tr in tr_elements:
        td_elements = tr.find_all("td")
        row = []
        if uri != "real-time-futures":
            td_elements.pop(4)
        for td in td_elements:
            row.append(td.text.strip())
        data.append(row)

    table = PrettyTable()
    table.field_names = [
        "commodity",
        "month",
        "last",
        "high",
        "low",
        "change",
        "% change",
        "time",
    ]
    for row in data:
        table.add_row(utils.format_string(row[1:9]))

    table.align["commodity"] = "l"
    table = utils.green_red_colouring(table, indices=[5, 6])

    return f"{str(table)}"


# Command functions
def cush():
    response = httpx.get(
        "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=W_EPC0_SAX_YCUOK_MBBL&f=W"
    )
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", class_="FloatTitle")
    tr_elements = table.find("tbody").find_all("tr")
    data = []
    for tr in tr_elements:
        td_elements = tr.find_all("td")
        row = []
        for td in td_elements:
            row.append(td.text.strip())
        data.append(row)

    table = PrettyTable()
    table.field_names = [
        "date",
        "w1 end",
        "w1 bbl",
        "w2 end",
        "w2 bbl",
        "w3 end",
        "w3 bbl",
        "w4 end",
        "w4 bbl",
        "w5 end",
        "w5 bbl",
    ]
    count = 0
    for row in reversed(data):
        if len(row) == 11:
            table.add_row(row)
            count += 1
            if count >= 30:
                break

    return f"{str(table)}"


def elec():
    return spider.commodities_elec()


def energy():
    return commodity_table("energy")


def futures():
    response = httpx.get("https://www.investing.com/commodities/real-time-futures")
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table")
    tr_elements = table.find_all("tbody")[0].find_all("tr")
    data = []
    for tr in tr_elements:
        td_elements = tr.find_all("td")
        row = []
        for td in td_elements:
            row.append(td.text.strip())
        data.append(row)

    table = PrettyTable()
    table.field_names = [
        "commodity",
        "month",
        "last",
        "high",
        "low",
        "change",
        "% change",
        "time",
    ]
    for row in data:
        table.add_row(utils.format_string(row))

    table.align["commodity"] = "l"
    table = utils.green_red_colouring(table, indices=[5, 6])

    return f"{str(table)}"


def grains():
    return commodity_table("grains")


def indices():
    return spider.commodities_indices()


def meats():
    return commodity_table("meats")


def metals():
    return commodity_table("metals")


def news(lim: str = "12"):
    response = httpx.get("https://www.ft.com/commodities")
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.find(
        "ul", class_="o-teaser-collection__list js-stream-list"
    ).find_all("li")
    data = []
    for x in articles:
        try:
            title = x.find("div", class_="o-teaser__heading").text.strip()
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


# TODO
def quote(*symbols):
    return "coming soon..."


def softs():
    return commodity_table("softs")


# TODO
def symbols():
    return "coming soon..."
