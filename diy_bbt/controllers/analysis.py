import functools

import diy_bbt.providers.analysis.fundamental as fundamental
import diy_bbt.providers.analysis.portfolio as portfolio
import diy_bbt.providers.analysis.technical as technical
import diy_bbt.utils as utils
from diy_bbt.controllers.base import Base


# Controller classes for 'analysis' sections
class Fundamental(Base):
    def __init__(self):
        super().__init__()
        self.controllers.update(
            {
                "balance": fundamental.balance,
                "bl": fundamental.balance,
                "cashflow": fundamental.cashflow,
                "c": fundamental.cashflow,
                "comp": fundamental.comp,
                "cm": fundamental.comp,
                "dividends": fundamental.dividends,
                "dv": fundamental.dividends,
                "earndates": fundamental.earndates,
                "ed": fundamental.earndates,
                "earnhist": fundamental.earnhist,
                "eh": fundamental.earnhist,
                "earntrend": fundamental.earntrend,
                "et": fundamental.earntrend,
                "esg": fundamental.esg,
                "financials": fundamental.financials,
                "f": fundamental.financials,
                "holdmajor": fundamental.holdmajor,
                "hm": fundamental.holdmajor,
                "income": fundamental.income,
                "i": fundamental.income,
                "keystats": fundamental.keystats,
                "k": fundamental.keystats,
            }
        )
        self.cache = functools.lru_cache()

    def get_source(self):
        return fundamental

    def execute(self, cmd):
        if len(cmd) == 1:
            return self.name()
        elif cmd[1] in self.controllers:
            func = self.controllers[cmd[1]]
            options = (
                tuple(utils.get_elements_after_dash(cmd[2:])) if len(cmd) > 2 else ()
            )
            args = (
                tuple(utils.get_elements_before_dash(cmd[2:])) if len(cmd) > 2 else ()
            )
            if not options:
                return self.cache(func)(*args)
            return self.cache(func)(*args, options=options)
        return self.unknown(cmd)


class Portfolio(Base):
    def __init__(self):
        super().__init__()
        self.controllers.update(
            {
                "corr": portfolio.corr,
                "c": portfolio.corr,
                "meancorr": portfolio.meancorr,
                "mc": portfolio.meancorr,
                "returns": portfolio.returns,
                "r": portfolio.returns,
                "sumcorr": portfolio.sumcorr,
                "sc": portfolio.sumcorr,
                "variance": portfolio.variance,
                "v": portfolio.variance,
            }
        )
        self.cache = functools.lru_cache()

    def get_source(self):
        return portfolio

    def execute(self, cmd):
        if len(cmd) == 1:
            return self.name()
        elif cmd[1] in self.controllers:
            func = self.controllers[cmd[1]]
            if len(cmd) > 1:
                options = tuple(x for x in cmd[2:] if x.startswith("-"))
                args = list(x for x in cmd[2:] if not x.startswith("-"))
                if options:
                    return self.cache(func)(*args, options=options)
                return self.cache(func)(*args)
            return self.cache(func)(())
        return self.unknown(cmd)


class Technical(Base):
    def __init__(self):
        super().__init__()
        self.controllers.update(
            {
                "indicator": technical.indicator,
                "i": technical.indicator,
                "indlist": technical.indlist,
                "il": technical.indlist,
            }
        )
        self.cache = functools.lru_cache()

    def get_source(self):
        return technical

    def execute(self, cmd):
        if len(cmd) == 1:
            return self.name()
        elif cmd[1] in self.controllers:
            func = self.controllers[cmd[1]]
            args = cmd[2:] if len(cmd) > 1 else []
            return self.cache(func)(*args)
        return self.unknown(cmd)
