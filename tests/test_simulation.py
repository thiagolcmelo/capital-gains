import pytest

from src.operation import Operation
from src.simulation import Simulation
from src.tax import Tax
from src.tax_error import TaxError


@pytest.mark.parametrize(
    "tax, expected",
    [
        (0.0, Tax(0.0)),
        (0.55, Tax(0.55)),
        (0.555, Tax(0.56)),
    ],
)
def test_make_tax(tax, expected):
    assert Simulation.make_tax(tax) == expected


@pytest.mark.parametrize(
    "current_stocks, current_weighted_average, new_stocks, buy_price, expected",
    [
        (0, 0.23, 12, 1.03, 1.03),
        (10, 20.0, 5, 10.0, 16.67),
        (22, 1.0, 5, 0.46, 0.9),
        (30, 0.23, 42, 0.8, 0.56),
        (30, 1.05, 8, 0.47, 0.93),
        (41, 1.64, 20, 0.06, 1.12),
        (55, 0.25, 27, 0.67, 0.39),
        (65, 0.68, 88, 0.56, 0.61),
        (95, 1.63, 38, 0.79, 1.39),
    ],
)
def test_calculate_weighted_average(
    current_stocks, current_weighted_average, new_stocks, buy_price, expected
):
    assert Simulation.calculate_weighted_average(
        current_stocks, current_weighted_average, new_stocks, buy_price
    ) == pytest.approx(expected)


def test_buy():
    simulation = Simulation(0, 0.0, 0.0)
    operation = Operation("buy", 10.0, 1000)
    tax = simulation.buy(operation)
    assert tax == Tax(0.0)


def test_sell_non_taxable_under_limit():
    simulation = Simulation(0, 0.0, 0.0)
    buy_operation = Operation("buy", 10.0, 10)
    _ = simulation.buy(buy_operation)
    sell_operation = Operation("sell", 10.0, 5)
    tax = simulation.sell(sell_operation)
    assert tax == Tax(0.0)


def test_sell_non_taxable_after_loss():
    simulation = Simulation(0, 0.0, 0.0)
    buy_operation = Operation("buy", 10.0, 10000)
    _ = simulation.buy(buy_operation)
    sell_operation = Operation("sell", 5.0, 10000)
    tax = simulation.sell(sell_operation)
    assert tax == Tax(0.0)


def test_sell_taxable():
    simulation = Simulation(0, 0.0, 0.0)
    buy_operation = Operation("buy", 10.0, 10000)
    _ = simulation.buy(buy_operation)
    sell_operation = Operation("sell", 20.0, 5000)
    tax = simulation.sell(sell_operation)
    assert tax == Tax(10000.0)


def test_sell_invalid_quantity():
    simulation = Simulation(0, 0.0, 0.0)
    buy_operation = Operation("buy", 10.0, 10000)
    _ = simulation.buy(buy_operation)
    sell_operation = Operation("sell", 20.0, 11000)
    result = simulation.sell(sell_operation)
    assert type(result) is TaxError
    assert result.error == "Can't sell more stocks than you have"
