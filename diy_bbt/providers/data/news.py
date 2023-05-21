import os

import httpx
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable

import diy_bbt.utils as utils

api_key = os.environ["KEY_NEWS_API"]

NEWS_MENU = {
    "country, c": "headlines by country",
    "earn, er": "today's earnings",
    "ecev, ec": "today's economic events",
    "energy, e": "energy sector headlines",
    "fin, f": "financial sector headlines",
    "health, hl": "health sector headlines",
    "ind, i": "industrials sector headlines",
    "media, m": "media sector headlines",
    "pro, p": "professional services sector headlines",
    "ret, r": "retail & consumer sector headlines",
    "source, s": "headlines by news source",
    "srclist, sl": "news source list by industry",
    "tech, tc": "technology sector headlines",
    "tele, tl": "telecoms sector headlines",
    "topic, t": "headlines by topic",
    "tran, tr": "transport sector headlines",
}


# Helper functions
def help():
    return utils.help(menu=NEWS_MENU, home=False)


def string():
    return "news"


def ft_news(title, lim):
    response = httpx.get(f"https://www.ft.com/{title}")
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


# Command functions
def country(name="US"):
    try:
        data = requests.get(
            f"https://newsapi.org/v2/top-headlines?country={name.upper()}&category=business&apiKey={api_key}"
        ).json()
    except KeyboardInterrupt:
        return
    table = PrettyTable()
    table.field_names = ["title", "author", "published"]
    for item in data["articles"]:
        table.add_row([item["title"], item["author"], item["publishedAt"]])

    table._max_width = {"title": 90}
    table.align = "l"

    return f"{str(table)}"


def earn():
    response = httpx.get("https://www.investing.com/earnings-calendar/")
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", id="earningsCalendarData")
    day = table.find_all("td", class_="theDay")[0].text
    tr_elements = table.find_all("tbody")[0].find_all("tr")
    data = []
    for tr in tr_elements[1:]:
        td_elements = tr.find_all("td")
        row = []
        for td in td_elements:
            row.append(td.text.strip())
        row = row[1:7]
        data.append(row)

    table = PrettyTable()
    table.field_names = [
        "date",
        "company",
        "eps",
        "eps forecast",
        "revenue",
        "rev. forecast",
        "market cap",
    ]
    count = 0
    for row in data:
        if row:
            row[2] = row[2].replace("/\xa0\xa0", "")
            row[4] = row[4].replace("/\xa0\xa0", "")
            table.add_row(utils.format_string([day] + row))
            count += 1
            if count >= 20:
                break

    table.align["company"] = "l"

    return f"{str(table)}"


def ecev():
    response = httpx.get("https://www.investing.com/economic-calendar/")
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", id="economicCalendarData")
    day = table.find_all("td", class_="theDay")[0].text
    tr_elements = table.find_all("tr", class_="js-event-item")
    data = []
    for tr in tr_elements:
        td_elements = tr.find_all("td")
        row = []
        for td in td_elements:
            row.append(td.text.strip())
        data.append(row)

    table = PrettyTable()
    table.field_names = ["time", "currency", "event", "actual", "forecast", "previous"]
    for row in data:
        row = row[:2] + row[3:7]
        table.add_row(utils.format_string([day + " " + row[0]] + row[1:]))

    table.align["event"] = "l"

    return f"{str(table)}"


def energy(lim: str = "12"):
    return ft_news("energy", lim)


def fin(lim: str = "12"):
    return ft_news("financials", lim)


def health(lim: str = "12"):
    return ft_news("health", lim)


def ind(lim: str = "12"):
    return ft_news("industrials", lim)


def media(lim: str = "12"):
    return ft_news("media", lim)


def pro(lim: str = "12"):
    return ft_news("professional-services", lim)


def ret(lim: str = "12"):
    return ft_news("retail-consumer", lim)


def source(name="bbc-news"):
    try:
        data = requests.get(
            f"https://newsapi.org/v2/top-headlines?sources={name}&apiKey={api_key}"
        ).json()
    except KeyboardInterrupt:
        return
    table = PrettyTable()
    table.field_names = ["title", "author", "published"]
    for item in data["articles"]:
        table.add_row([item["title"], item["author"], item["publishedAt"]])

    table._max_width = {"title": 90}
    table.align = "l"

    return f"{str(table)}"


def srclist(category=None):
    try:
        if category:
            data = requests.get(
                f"https://newsapi.org/v2/top-headlines/sources?category={category}&apiKey={api_key}"
            ).json()
        else:
            data = requests.get(
                f"https://newsapi.org/v2/top-headlines/sources?&apiKey={api_key}"
            ).json()
    except KeyboardInterrupt:
        return
    table = PrettyTable()
    table.field_names = ["id", "category", "description"]
    for item in data["sources"]:
        if item["id"] not in (
            "aftenposten",
            "ansa",
            "argaam",
            "blasting-news-br",
            "bild",
            "cnn-es",
            "die-zeit",
            "el-mundo",
            "focus",
            "globo",
            "google-news-br",
            "google-news-fr",
            "google-news-is",
            "google-news-it",
            "google-news-ru",
            "google-news-sa",
            "goteborgs-posten",
            "gruenderszene",
            "handelsblatt",
            "il-sole-24-ore",
            "infobae",
            "info-money",
            "la-gaceta",
            "la-nacion",
            "la-repubblica",
            "le-monde",
            "lenta",
            "lequipe",
            "les-echos",
            "liberation",
            "marca",
            "nrk",
            "rbc",
            "rt",
            "rtl-nieuws",
            "sabq",
            "spiegel-online",
            "svenska-dagbladet",
            "t3",
            "wirtschafts-woche",
            "xinhua-net",
            "ynet",
        ):
            description = item["description"][:140]
            if description[-1] != ".":
                description += "..."
            table.add_row([item["id"], item["category"], description])

    table._max_width = {"id": 40, "description": 60}
    table.align = "l"

    return f"{str(table)}"


def tech(lim: str = "12"):
    return ft_news("technology-sector", lim)


def tele(lim: str = "12"):
    return ft_news("telecoms", lim)


def topic(name="finance"):
    try:
        data = requests.get(
            f"https://newsapi.org/v2/top-headlines?q={name}&apiKey={api_key}"
        ).json()
    except KeyboardInterrupt:
        return
    table = PrettyTable()
    table.field_names = ["title", "author", "published"]
    for item in data["articles"]:
        table.add_row([item["title"], item["author"], item["publishedAt"]])

    table._max_width = {"title": 60}
    table.align["title"] = "l"
    table.align["author"] = "l"

    return f"{str(table)}"


def tran(lim: str = "12"):
    return ft_news("transport", lim)
