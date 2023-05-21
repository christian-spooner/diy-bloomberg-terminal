import diy_bbt.utils as utils

HOME_MENU = {
    "alternative, a": "hedge funds, real estate, art",
    "commodities, c": "metals, energy, food, softs",
    "credit, cd": "bonds, treasuries, money market",
    "crypto, cp": "bitcoin, altcoins, defi, nfts",
    "derivatives, d": "options, futures, swaps, forwards",
    "equities, e": "stocks, etfs, indices, mutual funds",
    "forex, f": "currencies, exchange rates",
    "macro, m": "GDP, interest rates, inflation",
    "misc, ms": "social media, open source, covid",
    "news, n": "headlines, upcoming events",
    "fundamental, fn": "fundamental analysis",
    "portfolio, p": "portfolio optimisation",
    "technical, t": "technical analysis",
    "back, b": "back to previous menu",
    "clear, cl": "clear the terminal",
    "exit, ^C": "exit the terminal",
    "help, h": "display menu items",
    "settings, s": "terminal settings",
}


def string():
    return "home"


def help():
    return utils.help(menu=HOME_MENU, home=True)
