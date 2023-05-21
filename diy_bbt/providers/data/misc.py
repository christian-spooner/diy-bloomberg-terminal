import csv
import os
from datetime import datetime

import colorama
import httpx
import requests
import wikipediaapi as w
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from selenium import webdriver
from selenium.webdriver.firefox.service import Service

import diy_bbt.providers.utils.spider as spider
import diy_bbt.utils as utils

api_key = os.environ["KEY_RAPID_API"]
geckodriver = os.environ["GECKODRIVER_PATH"]

MISC_MENU = {
    "1y": "1 year fixed rate bond rankings (UK)",
    "commons, cm": "members of the house of commons",
    "countries, c": "list of countries with alpha-2 codes",
    "easy, e": "easy access account rankings (UK)",
    "forbes, f": "richest people in the world",
    "fisc, fs": "fiscal year table",
    "funds, fn": "top global funds by assets",
    "gtrend, gt": "trending google searches",
    "insider, i": "latest insider trading",
    "pypl, p": "pypl index programming language rankings",
    "pypldb, pd": "pypl index database rankings",
    "reddit, r": "wall street bets sentiment",
    "regular, rg": "regular saver rankings (UK)",
    "richuk, rk": "richest people in the UK",
    "taxc, tc": "UK corporation tax tables",
    "taxi, ti": "UK income tax tables",
    "tiobe, t": "tiobe index programming language rankings",
    "twitter, tw": "trending twitter topics by country",
    "wikipedia, w": "wikipedia summary",
}


# Helper functions
def help():
    return utils.help(menu=MISC_MENU, home=False)


def string():
    return "misc"


# Command functions
def oneyear(lim: str = "12"):
    response = httpx.get("https://www.thesavings.guru/fixed-rate-bonds/1-year-fixed")
    soup = BeautifulSoup(response.content, "html.parser")
    rows = soup.find("tbody").find_all("tr", class_="content-row")
    data = []
    for x in rows:
        content = x.find_all("td")
        data.append(
            [content[0].find("img").get("alt").strip(), content[1].text.strip()]
        )

    data = sorted(data, key=lambda x: x[1], reverse=True)
    table = PrettyTable()
    table.field_names = ["name", "rate"]
    count = 0
    for row in data:
        table.add_row(row)
        if count > int(lim):
            break
        count += 1

    table.align = "l"

    return f"{str(table)}"


def commons():
    data = requests.get(
        "https://lda.data.parliament.uk/commonsmembers.json?_pageSize=10000"
    ).json()["result"]["items"]
    table = PrettyTable()
    table.field_names = ["name", "party", "constituency"]
    for item in data:
        name = item["fullName"]["_value"]
        row = [
            name.split(" ", 1)[1] if name.startswith(("Mr ", "Ms ", "Mrs ")) else name,
            item["party"]["_value"] if "party" in item else "n/a",
            item["constituency"]["label"]["_value"]
            if "constituency" in item
            else "n/a",
        ]
        table.add_row(row)

    def party_colouring(party: str):
        if (
            party.startswith("Conservative")
            or party.startswith("Ulster")
            or party.endswith("Conservative")
        ):
            return colorama.Fore.BLUE + party + colorama.Style.RESET_ALL
        if (
            party.startswith("Labour")
            or party.startswith("Democratic")
            or party.startswith("Social")
            or party.endswith("Labour")
        ):
            return colorama.Fore.RED + party + colorama.Style.RESET_ALL
        if (
            party.startswith("Liberal")
            or party.startswith("Scottish")
            or party.startswith("Plaid")
            or party.startswith("Alliance")
        ):
            return colorama.Fore.YELLOW + party + colorama.Style.RESET_ALL
        if party.startswith("Green") or party.startswith("Sinn"):
            return colorama.Fore.GREEN + party + colorama.Style.RESET_ALL
        if party.startswith("UK"):
            return colorama.Fore.MAGENTA + party + colorama.Style.RESET_ALL
        return party

    for row in table.rows:
        row[1] = party_colouring(row[1])

    return f"{str(table)}"


def countries():
    data = []
    with open("diy_bbt/storage/files/country_codes.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)

    table = PrettyTable()
    for pair in data:
        table.add_row(
            utils.format_string(
                [colorama.Fore.BLUE + pair[0] + colorama.Style.RESET_ALL, pair[1]]
            )
        )

    table.align = "l"
    table.header = False

    return f"{str(table)}"


def easy(lim: str = "12"):
    response = httpx.get("https://www.thesavings.guru/saving-accounts/easy-access")
    soup = BeautifulSoup(response.content, "html.parser")
    rows = soup.find("tbody").find_all("tr")
    data = []
    for x in rows:
        content = x.find_all("td")
        data.append(
            [content[0].find("img").get("alt").strip(), content[1].text.strip()]
        )

    data = sorted(data, key=lambda x: x[1], reverse=True)
    table = PrettyTable()
    table.field_names = ["name", "rate"]
    count = 0
    for row in data:
        table.add_row(row)
        if count > int(lim):
            break
        count += 1

    table.align = "l"

    return f"{str(table)}"


def forbes(lim: str = "20"):
    fields = (
        "rank,uri,personName,lastName,gender,source,industries,countryOfCitizenship,"
        "birthDate,finalWorth,estWorthPrev,imageExists,squareImage,listUri"
    )
    response = httpx.get(
        f"https://www.forbes.com/forbesapi/person/rtb/0/-estWorthPrev/true.json?fields={fields}"
    ).json()

    table = PrettyTable()
    table.field_names = ["rank", "name", "net worth ($B)", "source", "industry"]
    count = 0
    for row in response["personList"]["personsLists"]:
        vals = [*row.values()]
        table.add_row(
            [vals[1], vals[4], utils.format_float(vals[3]), vals[5], ",".join(vals[6])]
        )
        count += 1
        if count >= int(lim):
            break

    table.align = "l"

    return f"{str(table)}"


def fisc():
    data = []
    with open("diy_bbt/storage/files/fiscal_year.csv") as f:
        reader = csv.reader(f)
        data = [row for row in reader]

    table = PrettyTable()
    table.field_names = ["institution", "start date", "end date"]
    for row in data:
        table.add_row(row)

    table.align = "l"

    return f"{str(table)}"


def funds(lim: str = "12"):
    response = httpx.get("https://www.swfinstitute.org/fund-rankings")
    soup = BeautifulSoup(response.content, "html.parser")
    rows = soup.find("tbody").find_all("tr")
    data = []
    for x in rows:
        content = x.find_all("td")
        data.append([x.text.strip() for x in content])

    table = PrettyTable()
    table.field_names = ["rank", "name", "assets", "type", "region"]
    count = 0
    for row in data:
        table.add_row(row)
        count += 1
        if count >= int(lim):
            break

    table.align = "l"

    return f"{str(table)}"


def gtrend(country="US"):
    url = "https://google-trends8.p.rapidapi.com/trendings"
    querystring = {
        "region_code": country.upper(),
        "date": str(datetime.utcnow().date()),
        "hl": "en-US",
    }
    headers = {
        "X-RapidAPI-Key": "5959a4a0f2msh22a6830edc7d02ep17c38bjsn02ec5c70243b",
        "X-RapidAPI-Host": "google-trends8.p.rapidapi.com",
    }
    data = requests.request("GET", url, headers=headers, params=querystring).json()[
        "items"
    ]
    table = PrettyTable()
    table.field_names = ["query", "traffic"]
    for item in data:
        table.add_row(
            [
                utils.format_string(item["query"]),
                utils.format_string(item["formattedTraffic"]),
            ]
        )

    return f"{str(table)}"


def insider():
    return spider.misc_insider()


def pypl():
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    s = Service(geckodriver)
    driver = webdriver.Firefox(service=s, options=options)
    driver.get("https://pypl.github.io/PYPL.html")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find_all("tr")
    data = []
    for row in table:
        content = []
        for x in row:
            content.append(x.text.strip())
        data.append(content)

    table = PrettyTable()
    table.field_names = ["rank", "language", "share", "change"]
    count = 0
    for row in data[1:]:
        if len(row) == 6:
            row = row[1:]

        data = [row[0], row[2], row[3], row[4]]
        table.add_row(data)
        count += 1
        if count > 24:
            break

    table = utils.green_red_colouring(table, indices=[3])

    return f"{str(table)}"


def pypldb():
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    s = Service(geckodriver)
    driver = webdriver.Firefox(service=s, options=options)
    driver.get("https://pypl.github.io/DB.html")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find_all("tr")
    data = []
    for row in table:
        content = []
        for x in row:
            content.append(x.text.strip())
        data.append(content)

    table = PrettyTable()
    table.field_names = ["rank", "database", "share", "change"]
    count = 0
    for row in data[1:]:
        if len(row) == 6:
            row = row[1:]

        data = [row[0], row[2], row[3], row[4]]
        table.add_row(utils.format_string(data))
        count += 1
        if count > 24:
            break

    table = utils.green_red_colouring(table, indices=[3])

    return f"{str(table)}"


def reddit():
    data = requests.get("https://tradestie.com/api/v1/apps/reddit").json()
    table = PrettyTable()
    table.field_names = ["comments", "sentiment", "score", "ticker"]
    for item in data:
        table.add_row([x for x in item.values()])

    return f"{str(table)}"


def regular(lim: str = "12"):
    response = httpx.get("https://www.thesavings.guru/saving-accounts/regular-savings")
    soup = BeautifulSoup(response.content, "html.parser")
    rows = soup.find("tbody").find_all("tr", class_="content-row")
    data = []
    for x in rows:
        content = x.find_all("td")
        data.append(
            [content[0].find("img").get("alt").strip(), content[1].text.strip()]
        )

    data = sorted(data, key=lambda x: x[1], reverse=True)
    table = PrettyTable()
    table.field_names = ["name", "rate"]
    count = 0
    for row in data:
        table.add_row(row)
        if count > int(lim):
            break
        count += 1

    table.align = "l"

    return f"{str(table)}"


def richuk(lim: str = "20"):
    response = httpx.get("https://www.thetimes.co.uk/sunday-times-rich-list")
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("tbody").find_all("tr")
    data = []
    for x in table:
        row = x.find_all("td")
        data.append([y.text.strip() for y in row])

    table = PrettyTable()
    table.field_names = ["rank", "name", "net worth (£B)"]
    count = 0
    for row in data:
        table.add_row(row)
        if count > int(lim):
            break
        count += 1

    table.align = "l"

    return f"{str(table)}"


def taxc():
    data = []
    with open("diy_bbt/storage/files/tax/UK_corporation_tax.csv") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
    t1 = PrettyTable()
    t1.field_names = [
        "rate",
        "2023",
        "2022",
        "2021",
        "2020",
        "2019",
        "2018",
        "2017",
        "2016",
    ]
    for row in data:
        t1.add_row(
            [
                row["rate"],
                row["2023"],
                row["2022"],
                row["2021"],
                row["2020"],
                row["2019"],
                row["2018"],
                row["2017"],
                row["2016"],
            ]
        )
    t1.align["rate"] = "l"

    data = []
    with open("diy_bbt/storage/files/tax/UK_corporation_tax_rf.csv") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
    t2 = PrettyTable()
    t2.field_names = ["rate", "2023", "2022-2015"]
    for row in data:
        t2.add_row([row["rate"], row["2023"], row["2022-2015"]])
    t2.align["rate"] = "l"

    title_1 = "\033[1m" + "Corporation Tax" + "\033[0m"
    title_2 = "\033[1m" + "Corporation Tax (Ring Fence Companies)" + "\033[0m"

    return f"{title_1}\n{str(t1)}\n{title_2}\n{str(t2)}"


def taxi():
    data = []
    with open("diy_bbt/storage/files/tax/UK_income_tax.csv") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
    t1 = PrettyTable()
    t1.field_names = ["band", "taxable income (£)", "tax rate (%)"]
    for row in data:
        t1.add_row([row["band"], row["taxable income (£)"], row["tax rate (%)"]])
    t1.align["band"] = "l"

    data = []
    with open("diy_bbt/storage/files/tax/UK_savings_allowance.csv") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
    t2 = PrettyTable()
    t2.field_names = ["band", "allowance (£)"]
    for row in data:
        t2.add_row([row["band"], row["personal savings allowance (£)"]])
    t2.align["band"] = "l"

    t3 = PrettyTable()
    t3.field_names = ["type", "allowance (£)"]
    t3.add_row(["cash ", "20,000 (combined)"])
    t3.add_row(["stocks and shares", "20,000 (combined)"])
    t3.add_row(["innovative finance", "20,000 (combined)"])
    t3.add_row(["lifetime", "20,000 (combined)"])
    t3.align["type"] = "l"

    title_1 = "\033[1m" + "Income Tax" + "\033[0m"
    title_2 = "\033[1m" + "Personal Savings Allowance" + "\033[0m"
    title_3 = "\033[1m" + "ISAs" + "\033[0m"

    return f"{title_1}\n{str(t1)}\n{title_2}\n{str(t2)}\n{title_3}\n{str(t3)}"


def tiobe():
    response = httpx.get("https://www.tiobe.com/tiobe-index/")
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("tbody").find_all("tr")
    data = []
    for row in table:
        content = []
        for x in row:
            content.append(x.text.strip())
        data.append(content)

    table = PrettyTable()
    table.field_names = ["rank", "language", "share", "change"]
    for row in data:
        data = [row[0], row[4], row[5], row[6]]
        table.add_row(utils.format_string(data))

    table = utils.green_red_colouring(table, indices=[3])

    return f"{str(table)}"


def twitter(country="US"):
    COUNTRY_CODES = {}
    with open("diy_bbt/storage/files/country_codes.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            code, name = row
            COUNTRY_CODES[code] = name

    if country:
        country = COUNTRY_CODES[country.upper()].lower().replace(" ", "-")

    response = httpx.get(f"https://trends24.in/{country}")
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("div", id="trend-list")
    trend_card = table.find_all("div", class_="trend-card")[0].find("ol")
    li_elements = trend_card.find_all("li")
    data = []
    for li in li_elements:
        contents = li.contents
        if len(contents) > 1:
            data.append(
                [contents[0].text.strip().replace("#", ""), contents[2].text.strip()]
            )
        else:
            data.append([contents[0].text.strip().replace("#", ""), ""])

    table = PrettyTable()
    table.field_names = [
        "topic",
        "no. tweets",
    ]
    for row in data:
        table.add_row(utils.format_string(row))

    table.align["topic"] = "l"

    return f"{str(table)}"


def wikipedia(*args, options=()):
    topic = " ".join(args) if args else "finance"
    if "-l" in options:
        lim = int(options[options.index("-l") + 1])
    else:
        lim = 720
    wiki = w.Wikipedia("en")
    content = wiki.page(topic).summary[0:lim]
    if not content:
        content = f"no article found for `{topic}`"
    table = PrettyTable()
    table.add_row([content + "..."])
    table._max_width = {"Field 1": 90}
    table.align = "l"
    table.header = False

    return f"{str(table)}"
