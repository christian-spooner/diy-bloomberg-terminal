import pytest

from diy_bbt import Terminal

terminal = Terminal()
terminal.debug = True


alternative_cases = ["a hf", "a p", "a n", "a r", "a vc", "a z"]

commodities_cases = [
    "c c",
    "c e",
    "c en",
    "c f",
    "c g",
    "c m",
    "c mt",
    "c n",
    "c q",
    "c s",
    "c sm",
]

credit_cases = [
    "cd aaa",
    "cd cb",
    "cd cr",
    "cd em",
    "cd gs",
    "cd gy",
    "cd l",
    "cd n",
    "cd tr",
    "cd ty",
]

crypto_cases = [
    "cp a",
    "cp br",
    "cp c",
    "cp d",
    "cp e",
    "cp hk",
    "cp mc",
    "cp mp",
    "cp n",
    "cp nft",
    "cp p",
    "cp q",
    "cp s",
    "cp ts",
    "cp tn",
    "cp tvl",
    "cp v",
    "cp y",
]

derivatives_cases = [
    "d a msft",
    "d c",
    "d cl",
    "d ema msft",
    "d macd msft",
    "d n",
    "d p",
    "d rsi msft",
    "d sma msft",
]

equities_cases = [
    "e c",
    "e dg",
    "e dl",
    "e d",
    "e etf",
    "e ep",
    "e ex",
    "e i",
    "e if",
    "e m",
    "e mt",
    "e mp",
    "e n",
    "e p",
    "e q",
    "e s",
    "e sm",
    "e t",
]

forex_cases = ["f c", "f r", "f m", "f n", "f s"]

macro_cases = [
    "m cd",
    "m cpi",
    "m cu",
    "m gdp",
    "m gr",
    "m g",
    "m gu",
    "m i",
    "m is",
    "m lm",
    "m lw",
    "m m2",
    "m 2v",
    "m mg30",
    "m n",
    "m s",
    "m sp500",
    "m tt",
    "m ur",
    "m wl",
]

misc_cases = [
    "ms 1y",
    "ms cm",
    "ms c",
    "ms e",
    "ms f",
    "ms fs",
    "ms fn",
    "ms gt",
    "ms i",
    "ms p",
    "ms pd",
    "ms r",
    "ms rg",
    "ms ruk",
    "ms tc",
    "ms ti",
    "ms t",
    "ms tw",
    "ms w",
]

news_cases = ["n c", "n ec", "n er", "n e", "n s", "n sl", "n t"]


@pytest.mark.parametrize("command", alternative_cases)
def test_alternative(command):
    res = terminal.test(command)
    assert res != "n/a", f"Command '{command}' in section 'alternative' returned 'n/a'"


@pytest.mark.parametrize("command", commodities_cases)
def test_commodities(command):
    res = terminal.test(command)
    assert res != "n/a", f"Command '{command}' in section 'commodities' returned 'n/a'"


@pytest.mark.parametrize("command", credit_cases)
def test_credit(command):
    res = terminal.test(command)
    assert res != "n/a", f"Command '{command}' in section 'credit' returned 'n/a'"


@pytest.mark.parametrize("command", crypto_cases)
def test_crypto(command):
    res = terminal.test(command)
    assert res != "n/a", f"Command '{command}' in section 'crypto' returned 'n/a'"


@pytest.mark.parametrize("command", derivatives_cases)
def test_derivatives(command):
    res = terminal.test(command)
    assert res != "n/a", f"Command '{command}' in section 'derivatives' returned 'n/a'"


@pytest.mark.parametrize("command", equities_cases)
def test_equities(command):
    res = terminal.test(command)
    assert res != "n/a", f"Command '{command}' in section 'equities' returned 'n/a'"


@pytest.mark.parametrize("command", forex_cases)
def test_forex(command):
    res = terminal.test(command)
    assert res != "n/a", f"Command '{command}' in section 'forex' returned 'n/a'"


@pytest.mark.parametrize("command", macro_cases)
def test_macro(command):
    res = terminal.test(command)
    assert res != "n/a", f"Command '{command}' in section 'macro' returned 'n/a'"


@pytest.mark.parametrize("command", misc_cases)
def test_misc(command):
    res = terminal.test(command)
    assert res != "n/a", f"Command '{command}' in section 'misc' returned 'n/a'"


@pytest.mark.parametrize("command", news_cases)
def test_news(command):
    res = terminal.test(command)
    assert res != "n/a", f"Command '{command}' in section 'news' returned 'n/a'"
