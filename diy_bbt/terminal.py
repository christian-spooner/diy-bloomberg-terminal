import logging
import os
import readline
import sys

from diy_bbt.controllers.analysis import Fundamental, Portfolio, Technical
from diy_bbt.controllers.data import (Alternative, Commodities, Credit, Crypto,
                                      Derivatives, Equities, Forex, Macro,
                                      Misc, News)
from diy_bbt.controllers.home import Home
from diy_bbt.controllers.settings import Settings

logging.basicConfig(
    filename="./terminal_err.log",
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)


def back(terminal):
    terminal.path = ""


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def change_path(terminal, cmd):
    terminal.path = f"{cmd[1:]}"


class Terminal:
    def __init__(self):
        self.path = ""
        self.history = []
        self.debug = False
        self.home = Home()
        self.alternative = Alternative()
        self.commodities = Commodities()
        self.credit = Credit()
        self.crypto = Crypto()
        self.derivatives = Derivatives()
        self.equities = Equities()
        self.forex = Forex()
        self.macro = Macro()
        self.misc = Misc()
        self.news = News()
        self.fundamental = Fundamental()
        self.portfolio = Portfolio()
        self.technical = Technical()
        self.settings = Settings()
        self.controllers = {
            "alternative": self.alternative.execute,
            "a": self.alternative.execute,
            "commodities": self.commodities.execute,
            "c": self.commodities.execute,
            "credit": self.credit.execute,
            "cd": self.credit.execute,
            "crypto": self.crypto.execute,
            "cp": self.crypto.execute,
            "derivatives": self.derivatives.execute,
            "d": self.derivatives.execute,
            "equities": self.equities.execute,
            "e": self.equities.execute,
            "forex": self.forex.execute,
            "f": self.forex.execute,
            "macro": self.macro.execute,
            "m": self.macro.execute,
            "misc": self.misc.execute,
            "ms": self.misc.execute,
            "news": self.news.execute,
            "n": self.news.execute,
            "fundamental": self.fundamental.execute,
            "fn": self.fundamental.execute,
            "portfolio": self.portfolio.execute,
            "p": self.portfolio.execute,
            "technical": self.technical.execute,
            "t": self.technical.execute,
            "settings": self.settings.execute,
            "s": self.settings.execute,
        }

    def new_input(self):
        history_index = len(self.history)
        prompt = f"{self.path} $ " if self.path else "$ "
        line = input(f"{self.path} $ " if self.path else "$ ")
        if line == "\x1b[A":
            if self.history:
                history_index = max(0, history_index - 1)
                line = self.history[history_index]
                sys.stdout.write(prompt + line)
        elif line == "\x1b[B":
            if self.history:
                history_index = min(len(self.history), history_index + 1)
                line = (
                    self.history[history_index]
                    if history_index < len(self.history)
                    else ""
                )
                sys.stdout.write(prompt + line)
        else:
            history_index = len(self.history)
            self.history.append(line)
        return line

    def new_output(self, output: str):
        if output == "BACK":
            output = back(self)
        elif output == "CLEAR":
            return clear()
        elif output.startswith("/"):
            output = change_path(self, output)

        if self.path and output:
            output.removeprefix(self.path)

        if output:
            if self.debug:
                return output
            sys.stdout.write(f"{output}\n")

    def command_handler(self, cmd: list[str]):
        try:
            if cmd[0] != "":
                if self.path:
                    cmd = [self.path] + cmd
                func = self.controllers.get(cmd[0], self.home.execute)
                return self.new_output(func(cmd))
        except Exception as err:
            logging.error(err)
            return self.new_output("n/a")

    def run(self):
        readline.clear_history()
        clear()
        try:
            while True:
                new_input = self.new_input().lower()
                cmd = [x.strip() for x in new_input.split(" ") if x.strip()] or [""]
                if cmd[0] == "exit":
                    break
                self.command_handler(cmd)
        except KeyboardInterrupt:
            sys.stdout.write("\n")

    def test(self, input):
        cmd = input.split(" ")
        return self.command_handler(cmd)
