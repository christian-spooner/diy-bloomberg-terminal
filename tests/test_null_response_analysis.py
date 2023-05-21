import pytest

from diy_bbt import Terminal

terminal = Terminal()
terminal.debug = True


fundamental_cases = [
    "bl msft",
    "c msft",
    "cm msft",
    "dv msft",
    "ed msft",
    "eh msft",
    "et msft",
    "esg msft",
    "f msft",
    "hm msft",
    "i msft",
    "k msft",
    "v msft",
]

portfolio_cases = [
    "c msft aapl",
    "mcorr msft aapl googl",
    "r msft",
    "sc msft aapl google",
    "v msft",
]

technical_cases = [
    "i rsi msft",
]


@pytest.mark.parametrize("command", fundamental_cases)
def test_fundamental(command):
    res = terminal.test(command)
    assert res != "n/a", f"Command '{command}' in section 'fundamental' returned 'n/a'"


@pytest.mark.parametrize("command", portfolio_cases)
def test_portfolio(command):
    res = terminal.test(command)
    assert res != "n/a", f"Command '{command}' in section 'portfolio' returned 'n/a'"


@pytest.mark.parametrize("command", technical_cases)
def test_technical(command):
    res = terminal.test(command)
    assert res != "n/a", f"Command '{command}' in section 'technical' returned 'n/a'"
