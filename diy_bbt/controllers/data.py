import functools

import diy_bbt.providers.data.alternative as alternative
import diy_bbt.providers.data.commodities as commodities
import diy_bbt.providers.data.credit as credit
import diy_bbt.providers.data.crypto as crypto
import diy_bbt.providers.data.derivatives as derivatives
import diy_bbt.providers.data.equities as equities
import diy_bbt.providers.data.forex as forex
import diy_bbt.providers.data.macro as macro
import diy_bbt.providers.data.misc as misc
import diy_bbt.providers.data.news as news
import diy_bbt.utils as utils
from diy_bbt.controllers.base import Base


# Controller classes for 'data' sections
class Alternative(Base):
    def __init__(self):
        super().__init__()
        self.controllers.update(
            {
                "hedge": alternative.hedge,
                "hf": alternative.hedge,
                "priveq": alternative.priveq,
                "p": alternative.priveq,
                "news": alternative.news,
                "n": alternative.news,
                "reit": alternative.reit,
                "r": alternative.reit,
                "vcap": alternative.vcap,
                "vc": alternative.vcap,
                "zill": alternative.zill,
                "z": alternative.zill,
            }
        )
        self.cache = functools.lru_cache()

    def get_source(self):
        return alternative

    def execute(self, cmd):
        if len(cmd) == 1:
            return self.name()
        elif cmd[1] in self.controllers:
            func = self.controllers[cmd[1]]
            args = cmd[2:] if len(cmd) > 1 else []
            return self.cache(func)(*args)
        return self.unknown(cmd)


class Commodities(Base):
    def __init__(self):
        super().__init__()
        self.controllers.update(
            {
                "cush": commodities.cush,
                "c": commodities.cush,
                "elec": commodities.elec,
                "e": commodities.elec,
                "energy": commodities.energy,
                "en": commodities.energy,
                "futures": commodities.futures,
                "f": commodities.futures,
                "grains": commodities.grains,
                "g": commodities.grains,
                "indices": commodities.indices,
                "i": commodities.indices,
                "meats": commodities.meats,
                "m": commodities.meats,
                "metals": commodities.metals,
                "mt": commodities.metals,
                "news": commodities.news,
                "n": commodities.news,
                "quote": commodities.quote,
                "q": commodities.quote,
                "softs": commodities.softs,
                "s": commodities.softs,
                "symbols": commodities.symbols,
                "sm": commodities.symbols,
            }
        )
        self.cache = functools.lru_cache()

    def get_source(self):
        return commodities

    def execute(self, cmd):
        if len(cmd) == 1:
            return self.name()
        elif cmd[1] in self.controllers:
            func = self.controllers[cmd[1]]
            args = cmd[2:] if len(cmd) > 1 else []
            return self.cache(func)(*args)
        return self.unknown(cmd)


class Credit(Base):
    def __init__(self):
        super().__init__()
        self.controllers.update(
            {
                "aaabonds": credit.aaabonds,
                "aaa": credit.aaabonds,
                "cbrates": credit.cbrates,
                "cb": credit.cbrates,
                "corbonds": credit.corbonds,
                "cr": credit.corbonds,
                "embonds": credit.embonds,
                "em": credit.embonds,
                "govspr": credit.govspr,
                "gs": credit.govspr,
                "govyld": credit.govyld,
                "gy": credit.govyld,
                "libor": credit.libor,
                "l": credit.libor,
                "news": credit.news,
                "n": credit.news,
                "tryield": credit.tryield,
                "tr": credit.tryield,
                "tyield": credit.tyield,
                "ty": credit.tyield,
            }
        )
        self.cache = functools.lru_cache()

    def get_source(self):
        return credit

    def execute(self, cmd):
        if len(cmd) == 1:
            return self.name()
        elif cmd[1] in self.controllers:
            func = self.controllers[cmd[1]]
            args = cmd[2:] if len(cmd) > 1 else []
            return self.cache(func)(*args)
        return self.unknown(cmd)


class Crypto(Base):
    def __init__(self):
        super().__init__()
        self.controllers.update(
            {
                "airdrop": crypto.airdrop,
                "a": crypto.airdrop,
                "bridges": crypto.bridges,
                "br": crypto.bridges,
                "cxtran": crypto.cxtran,
                "c": crypto.cxtran,
                "deglob": crypto.deglob,
                "d": crypto.deglob,
                "exchanges": crypto.exchanges,
                "e": crypto.exchanges,
                "hacks": crypto.hacks,
                "hk": crypto.hacks,
                "mcap": crypto.mcap,
                "mc": crypto.mcap,
                "mperc": crypto.mperc,
                "mp": crypto.mperc,
                "news": crypto.news,
                "n": crypto.news,
                "nft": crypto.nft,
                "price": crypto.price,
                "p": crypto.price,
                "quote": crypto.quote,
                "q": crypto.quote,
                "stables": crypto.stables,
                "s": crypto.stables,
                "treasury": crypto.treasury,
                "ts": crypto.treasury,
                "trending": crypto.trending,
                "tn": crypto.trending,
                "tvl": crypto.tvl,
                "volume": crypto.volume,
                "v": crypto.volume,
                "yields": crypto.yields,
                "y": crypto.yields,
            }
        )
        self.cache = functools.lru_cache()

    def get_source(self):
        return crypto

    def execute(self, cmd):
        if len(cmd) == 1:
            return self.name()
        elif cmd[1] in self.controllers:
            func = self.controllers[cmd[1]]
            args = cmd[2:] if len(cmd) > 1 else []
            return self.cache(func)(*args)
        return self.unknown(cmd)


class Derivatives(Base):
    def __init__(self):
        super().__init__()
        self.controllers.update(
            {
                "aggregate": derivatives.aggregate,
                "a": derivatives.aggregate,
                "calls": derivatives.calls,
                "c": derivatives.calls,
                "contract": derivatives.contract,
                "cn": derivatives.contract,
                "ema": derivatives.ema,
                "macd": derivatives.macd,
                "news": derivatives.news,
                "n": derivatives.news,
                "puts": derivatives.puts,
                "p": derivatives.puts,
                "rsi": derivatives.rsi,
                "sma": derivatives.sma,
            }
        )
        self.cache = functools.lru_cache()

    def get_source(self):
        return derivatives

    def execute(self, cmd):
        if len(cmd) == 1:
            return self.name()
        elif cmd[1] in self.controllers:
            func = self.controllers[cmd[1]]
            args = cmd[2:] if len(cmd) > 1 else []
            return self.cache(func)(*args)
        return self.unknown(cmd)


class Equities(Base):
    def __init__(self):
        super().__init__()
        self.controllers.update(
            {
                "certs": equities.certs,
                "c": equities.certs,
                "daygain": equities.daygain,
                "dg": equities.daygain,
                "daylose": equities.daylose,
                "dl": equities.daylose,
                "description": equities.description,
                "d": equities.description,
                "etf": equities.etf,
                "etfp": equities.etfp,
                "ep": equities.etfp,
                "exchanges": equities.exchanges,
                "ex": equities.exchanges,
                "indices": equities.indices,
                "i": equities.indices,
                "indfut": equities.indfut,
                "if": equities.indfut,
                "mcap": equities.mcap,
                "m": equities.mcap,
                "mutf": equities.mutf,
                "mt": equities.mutf,
                "mutp": equities.mutp,
                "mp": equities.mutp,
                "news": equities.news,
                "n": equities.news,
                "price": equities.price,
                "p": equities.price,
                "quotemon": equities.quotemonitor,
                "qm": equities.quotemonitor,
                "quote": equities.quote,
                "q": equities.quote,
                "summary": equities.summary,
                "s": equities.summary,
                "symbol": equities.symbol,
                "sm": equities.symbol,
                "trending": equities.trending,
                "t": equities.trending,
            }
        )
        self.cache = functools.lru_cache()

    def get_source(self):
        return equities

    def execute(self, cmd):
        if len(cmd) == 1:
            return self.name()
        elif cmd[1] in self.controllers:
            func = self.controllers[cmd[1]]
            args = cmd[2:] if len(cmd) > 1 else []
            return self.cache(func)(*args)
        return self.unknown(cmd)


class Forex(Base):
    def __init__(self):
        super().__init__()
        self.controllers.update(
            {
                "convert": forex.convert,
                "c": forex.convert,
                "rate": forex.rate,
                "r": forex.rate,
                "mrate": forex.mrate,
                "m": forex.mrate,
                "news": forex.news,
                "n": forex.news,
                "series": forex.series,
                "s": forex.series,
            }
        )
        self.cache = functools.lru_cache()

    def get_source(self):
        return forex

    def execute(self, cmd):
        if len(cmd) == 1:
            return self.name()
        elif cmd[1] in self.controllers:
            func = self.controllers[cmd[1]]
            args = cmd[2:] if len(cmd) > 1 else []
            return self.cache(func)(*args)
        return self.unknown(cmd)


class Macro(Base):
    def __init__(self):
        super().__init__()
        self.controllers.update(
            {
                "comdep": macro.comdep,
                "cd": macro.comdep,
                "cpi": macro.cpi,
                "cpiuk": macro.cpiuk,
                "cu": macro.cpiuk,
                "gdp": macro.gdp,
                "gdpr": macro.gdpr,
                "gr": macro.gdpr,
                "gini": macro.gini,
                "g": macro.gini,
                "ginuk": macro.ginuk,
                "gk": macro.ginuk,
                "industry": macro.industry,
                "i": macro.industry,
                "israt": macro.israt,
                "is": macro.israt,
                "lmen": macro.lmen,
                "lm": macro.lmen,
                "lwmen": macro.lwmen,
                "lw": macro.lwmen,
                "m2": macro.m2,
                "m2vel": macro.m2vel,
                "2v": macro.m2vel,
                "mg30": macro.mg30,
                "news": macro.news,
                "n": macro.news,
                "sector": macro.sector,
                "s": macro.sector,
                "sp500": macro.sp500,
                "t10y2y": macro.t10y2y,
                "tt": macro.t10y2y,
                "unrate": macro.unrate,
                "ur": macro.unrate,
                "walcl": macro.walcl,
                "wl": macro.walcl,
            }
        )
        self.cache = functools.lru_cache()

    def get_source(self):
        return macro

    def execute(self, cmd):
        if len(cmd) == 1:
            return self.name()
        elif cmd[1] in self.controllers:
            func = self.controllers[cmd[1]]
            options = tuple(utils.get_elements_after_dash(cmd[1:]))
            if not options:
                return self.cache(func)()
            return self.cache(func)(options=options)
        return self.unknown(cmd)


class Misc(Base):
    def __init__(self):
        super().__init__()
        self.controllers.update(
            {
                "1y": misc.oneyear,
                "commons": misc.commons,
                "cm": misc.commons,
                "countries": misc.countries,
                "c": misc.countries,
                "easy": misc.easy,
                "e": misc.easy,
                "forbes": misc.forbes,
                "f": misc.forbes,
                "fisc": misc.fisc,
                "fs": misc.fisc,
                "funds": misc.funds,
                "fn": misc.funds,
                "gtrend": misc.gtrend,
                "gt": misc.gtrend,
                "insider": misc.insider,
                "i": misc.insider,
                "pypl": misc.pypl,
                "p": misc.pypl,
                "pypldb": misc.pypldb,
                "pd": misc.pypldb,
                "reddit": misc.reddit,
                "r": misc.reddit,
                "regular": misc.regular,
                "rg": misc.regular,
                "richuk": misc.richuk,
                "rk": misc.richuk,
                "taxc": misc.taxc,
                "tc": misc.taxc,
                "taxi": misc.taxi,
                "ti": misc.taxi,
                "tiobe": misc.tiobe,
                "t": misc.tiobe,
                "twitter": misc.twitter,
                "tw": misc.twitter,
                "wiki": misc.wikipedia,
                "w": misc.wikipedia,
            }
        )
        self.cache = functools.lru_cache()

    def get_source(self):
        return misc

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


class News(Base):
    def __init__(self):
        super().__init__()
        self.controllers.update(
            {
                "country": news.country,
                "c": news.country,
                "ecev": news.ecev,
                "ec": news.ecev,
                "earn": news.earn,
                "er": news.earn,
                "energy": news.energy,
                "e": news.energy,
                "fin": news.fin,
                "f": news.fin,
                "health": news.health,
                "hl": news.health,
                "ind": news.ind,
                "i": news.ind,
                "media": news.media,
                "m": news.media,
                "pro": news.pro,
                "p": news.pro,
                "ret": news.ret,
                "r": news.ret,
                "srclist": news.srclist,
                "sl": news.srclist,
                "tech": news.tech,
                "tc": news.tech,
                "tele": news.tele,
                "tl": news.tele,
                "topic": news.topic,
                "t": news.topic,
                "tran": news.tran,
                "tr": news.tran,
            }
        )
        self.cache = functools.lru_cache()

    def get_source(self):
        return news

    def execute(self, cmd):
        if len(cmd) == 1:
            return self.name()
        elif cmd[1] in self.controllers:
            func = self.controllers[cmd[1]]
            args = cmd[2:] if len(cmd) > 1 else []
            return self.cache(func)(*args)
        return self.unknown(cmd)
