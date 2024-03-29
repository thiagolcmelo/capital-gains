from src.tax_calculator import TaxCalculator
from src.operation import Operation
from src.tax import Tax
from src.tax_error import TaxError
from tests.utils import assert_tax_list_equal, simulations


def test_tax_calculator(simulations):
    for simulation in simulations:
        operations = [
            Operation(op["operation"], op["unit-cost"], op["quantity"])
            for op in simulation["input"]
        ]
        expected = [
            Tax(tx["tax"]) if "tax" in tx else TaxError(tx["error"])
            for tx in simulation["output"]
        ]
        actual = TaxCalculator.calculate(operations)
        label = simulation["label"]
        assert_tax_list_equal(actual, expected, label)
