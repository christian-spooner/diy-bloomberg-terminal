import colorama
from prettytable import PrettyTable

import diy_bbt.utils as utils


def commodities_elec(response):
    tr_elements = response.css("table")[-1].css("tr")
    data = []
    for tr in tr_elements[1:]:
        data.append(
            [
                " ".join(x.css("::text").getall())
                .replace("  ", "")
                .replace("\r\n", "")
                .replace("  ", "")
                .strip()
                for x in tr.css("td")
            ]
        )

    table = PrettyTable()
    table.field_names = [
        "country",
        "unit",
        "price",
        "day",
        "weekly",
        "monthly",
        "YoY",
        "date",
    ]
    for row in data:
        table.add_row(row)

    table.align["country"] = "l"
    for i, row in enumerate(table.rows):
        if i == 0:
            row[0] = row[0].replace(" GBP/MWh", "")
            row[2] = row[1]
            row[1] = "GBP/MWh"
        elif i == 2:
            row[0] = row[0].replace(" EUR/MWh", "")
            row[2] = row[1]
            row[1] = "EUR/MWh"
        else:
            row[0] = row[0].replace("EUR/MWh", "")
            row[2] = row[1]
            row[1] = "EUR/MWh"
    table = utils.green_red_colouring(table, indices=[3, 4, 5, 6])

    return str(table)


def commodities_indices(response):
    tr_elements = response.css("table")[-2].css("tr")
    data = []
    for tr in tr_elements[1:]:
        td = tr.css("td")
        content = [
            " ".join(x.css("::text").getall())
            .replace("  ", "")
            .replace("\r\n", "")
            .replace("  ", "")
            .strip()
            for x in td[1:]
        ]
        data.append([td[0].css("::text")[2].get()] + content)

    table = PrettyTable()
    table.field_names = [
        "index",
        "price",
        "day",
        "%",
        "weekly",
        "monthly",
        "YoY",
        "date",
    ]
    for row in data:
        table.add_row(row)

    table.align["index"] = "l"
    table = utils.green_red_colouring(table, indices=[3, 4, 5, 6])

    return str(table)


def macro_industry(response):
    tr_elements = response.css("table.table-light")[0].css("tr")
    data = []
    for tr in tr_elements:
        data.append([x.css("::text").get() for x in tr.css("td")])

    table = PrettyTable()
    for row in data[1:]:
        table.add_row(row)

    table.field_names = [
        "no.",
        "name",
        "stocks",
        "market cap ($)",
        "dividend",
        "p/e",
        "fwd p/e",
        "peg",
        "float short",
        "change",
        "volume",
    ]
    table.align["name"] = "l"
    for row in table.rows:
        row[1] = utils.format_string(row[1])

    table = utils.green_red_colouring(table, indices=[9])
    table.del_column("fwd p/e")
    table.del_column("stocks")

    return str(table)


def macro_sector(response):
    tr_elements = response.css("table.table-light")[0].css("tr")
    data = []
    for tr in tr_elements:
        data.append([x.css("::text").get() for x in tr.css("td")])

    table = PrettyTable()
    for row in data[1:]:
        table.add_row(row)

    table.field_names = [
        "no.",
        "name",
        "stocks",
        "market cap ($)",
        "dividend",
        "p/e",
        "fwd p/e",
        "peg",
        "float short",
        "change",
        "volume",
    ]
    table.align["name"] = "l"
    for row in table.rows:
        row[1] = utils.format_string(row[1])

    table = utils.green_red_colouring(table, indices=[9])
    table.del_column("fwd p/e")
    table.del_column("stocks")

    return str(table)


def macro_insider(response):
    tr_elements = response.css("table.table-insider")[0].css("tr")
    data = []
    for tr in tr_elements:
        data.append([x.css("::text").get() for x in tr.css("td")])

    table = PrettyTable()
    for row in data[1:]:
        table.add_row(row)

    def txn_colouring(txn: str):
        if txn == "Buy":
            return colorama.Fore.GREEN + txn + colorama.Style.RESET_ALL
        if txn == "Sale":
            return colorama.Fore.RED + txn + colorama.Style.RESET_ALL
        return txn

    table.del_column("Field 10")
    table.field_names = [
        "ticker",
        "owner",
        "relationship",
        "date",
        "txn",
        "cost",
        "#shares",
        "value ($)",
        "#shares total",
    ]
    table = table[:24]
    for row in table.rows:
        row[4] = txn_colouring(row[4])

    return str(table)
