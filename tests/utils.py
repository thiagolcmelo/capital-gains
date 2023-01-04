import io, sys

import pytest

from contextlib import contextmanager
from glob import glob
from json import loads
from os import path
from typing import Any, List

from src.operation import Operation
from src.tax import Tax


def assert_operation_list_equal(
    actual: List[Operation], expected: List[Operation], label: str
) -> None:
    assert len(actual) == len(expected), label
    for a, e in zip(actual, expected):
        assert a == e, label


def assert_tax_list_equal(actual: List[Tax], expected: List[Tax], label: str) -> None:
    assert len(actual) == len(expected), label
    for a, e in zip(actual, expected):
        assert a.tax == pytest.approx(e.tax), label


def assert_tax_output_equal(actual: str, expected: str, label: str) -> None:
    actual = [l.strip() for l in actual.split("\n") if l != ""]
    expected = [l.strip() for l in expected.split("\n") if l != ""]
    assert len(actual) == len(expected), label
    for a, e in zip(actual, expected):
        a = [Tax(tx["tax"]) for tx in loads(a)]
        e = [Tax(tx["tax"]) for tx in loads(e)]
        assert_tax_list_equal(a, e, label)


@pytest.fixture
def data_cases_input_filenames():
    return sorted(glob(path.join("tests", "data", "case_*", "input.txt")))


@pytest.fixture
def data_cases_output_filenames():
    return sorted(glob(path.join("tests", "data", "case_*", "output.txt")))


@contextmanager
def captured_output():
    new_out, new_err = io.StringIO(), io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


@pytest.fixture
def simulations():
    return [
        {
            "label": "case_01",
            "input": [
                {"operation": "buy", "unit-cost": 10.00, "quantity": 100},
                {"operation": "sell", "unit-cost": 15.00, "quantity": 50},
                {"operation": "sell", "unit-cost": 15.00, "quantity": 50},
            ],
            "output": [{"tax": 0.00}, {"tax": 0.00}, {"tax": 0.00}],
        },
        {
            "label": "case_02",
            "input": [
                {"operation": "buy", "unit-cost": 10.00, "quantity": 10000},
                {"operation": "sell", "unit-cost": 20.00, "quantity": 5000},
                {"operation": "sell", "unit-cost": 5.00, "quantity": 5000},
            ],
            "output": [{"tax": 0.00}, {"tax": 10000.00}, {"tax": 0.00}],
        },
        {
            "label": "case_03",
            "input": [
                {"operation": "buy", "unit-cost": 10.00, "quantity": 10000},
                {"operation": "sell", "unit-cost": 5.00, "quantity": 5000},
                {"operation": "sell", "unit-cost": 20.00, "quantity": 3000},
            ],
            "output": [{"tax": 0.00}, {"tax": 0.00}, {"tax": 1000.00}],
        },
        {
            "label": "case_04",
            "input": [
                {"operation": "buy", "unit-cost": 10.00, "quantity": 10000},
                {"operation": "buy", "unit-cost": 25.00, "quantity": 5000},
                {"operation": "sell", "unit-cost": 15.00, "quantity": 10000},
            ],
            "output": [{"tax": 0.00}, {"tax": 0.00}, {"tax": 0.00}],
        },
        {
            "label": "case_05",
            "input": [
                {"operation": "buy", "unit-cost": 10.00, "quantity": 10000},
                {"operation": "buy", "unit-cost": 25.00, "quantity": 5000},
                {"operation": "sell", "unit-cost": 15.00, "quantity": 10000},
                {"operation": "sell", "unit-cost": 25.00, "quantity": 5000},
            ],
            "output": [{"tax": 0.00}, {"tax": 0.00}, {"tax": 0.00}, {"tax": 10000.00}],
        },
        {
            "label": "case_06",
            "input": [
                {"operation": "buy", "unit-cost": 10.00, "quantity": 10000},
                {"operation": "sell", "unit-cost": 2.00, "quantity": 5000},
                {"operation": "sell", "unit-cost": 20.00, "quantity": 2000},
                {"operation": "sell", "unit-cost": 20.00, "quantity": 2000},
                {"operation": "sell", "unit-cost": 25.00, "quantity": 1000},
            ],
            "output": [
                {"tax": 0.00},
                {"tax": 0.00},
                {"tax": 0.00},
                {"tax": 0.00},
                {"tax": 3000.00},
            ],
        },
        {
            "label": "case_07",
            "input": [
                {"operation": "buy", "unit-cost": 10.00, "quantity": 10000},
                {"operation": "sell", "unit-cost": 2.00, "quantity": 5000},
                {"operation": "sell", "unit-cost": 20.00, "quantity": 2000},
                {"operation": "sell", "unit-cost": 20.00, "quantity": 2000},
                {"operation": "sell", "unit-cost": 25.00, "quantity": 1000},
                {"operation": "buy", "unit-cost": 20.00, "quantity": 10000},
                {"operation": "sell", "unit-cost": 15.00, "quantity": 5000},
                {"operation": "sell", "unit-cost": 30.00, "quantity": 4350},
                {"operation": "sell", "unit-cost": 30.00, "quantity": 650},
            ],
            "output": [
                {"tax": 0.00},
                {"tax": 0.00},
                {"tax": 0.00},
                {"tax": 0.00},
                {"tax": 3000.00},
                {"tax": 0.00},
                {"tax": 0.00},
                {"tax": 3700.00},
                {"tax": 0.00},
            ],
        },
        {
            "label": "case_08",
            "input": [
                {"operation": "buy", "unit-cost": 10.00, "quantity": 10000},
                {"operation": "sell", "unit-cost": 50.00, "quantity": 10000},
                {"operation": "buy", "unit-cost": 20.00, "quantity": 10000},
                {"operation": "sell", "unit-cost": 50.00, "quantity": 10000},
            ],
            "output": [
                {"tax": 0.00},
                {"tax": 80000.00},
                {"tax": 0.00},
                {"tax": 60000.00},
            ],
        },
    ]


@pytest.fixture
def data_cases_parsed():
    return [
        {
            "label": "case_01",
            "input": [
                [
                    Operation("buy", 10.00, 100),
                    Operation("sell", 15.00, 50),
                    Operation("sell", 15.00, 50),
                ]
            ],
            "output": [[Tax(0.00), Tax(0.00), Tax(0.00)]],
        },
        {
            "label": "case_02",
            "input": [
                [
                    Operation("buy", 10.00, 10000),
                    Operation("sell", 20.00, 5000),
                    Operation("sell", 5.00, 5000),
                ]
            ],
            "output": [[Tax(0.00), Tax(10000.00), Tax(0.00)]],
        },
        {
            "label": "case_03",
            "input": [
                [
                    Operation("buy", 10.00, 10000),
                    Operation("sell", 5.00, 5000),
                    Operation("sell", 20.00, 3000),
                ]
            ],
            "output": [[Tax(0.00), Tax(0.00), Tax(1000.00)]],
        },
        {
            "label": "case_04",
            "input": [
                [
                    Operation("buy", 10.00, 10000),
                    Operation("buy", 25.00, 5000),
                    Operation("sell", 15.00, 10000),
                ]
            ],
            "output": [[Tax(0.00), Tax(0.00), Tax(0.00)]],
        },
        {
            "label": "case_05",
            "input": [
                [
                    Operation("buy", 10.00, 10000),
                    Operation("buy", 25.00, 5000),
                    Operation("sell", 15.00, 10000),
                    Operation("sell", 25.00, 5000),
                ]
            ],
            "output": [[Tax(0.00), Tax(0.00), Tax(0.00), Tax(10000.00)]],
        },
        {
            "label": "case_06",
            "input": [
                [
                    Operation("buy", 10.00, 10000),
                    Operation("sell", 2.00, 5000),
                    Operation("sell", 20.00, 2000),
                    Operation("sell", 20.00, 2000),
                    Operation("sell", 25.00, 1000),
                ]
            ],
            "output": [
                [
                    Tax(0.00),
                    Tax(0.00),
                    Tax(0.00),
                    Tax(0.00),
                    Tax(3000.00),
                ]
            ],
        },
        {
            "label": "case_07",
            "input": [
                [
                    Operation("buy", 10.00, 10000),
                    Operation("sell", 2.00, 5000),
                    Operation("sell", 20.00, 2000),
                    Operation("sell", 20.00, 2000),
                    Operation("sell", 25.00, 1000),
                    Operation("buy", 20.00, 10000),
                    Operation("sell", 15.00, 5000),
                    Operation("sell", 30.00, 4350),
                    Operation("sell", 30.00, 650),
                ]
            ],
            "output": [
                [
                    Tax(0.00),
                    Tax(0.00),
                    Tax(0.00),
                    Tax(0.00),
                    Tax(3000.00),
                    Tax(0.00),
                    Tax(0.00),
                    Tax(3700.00),
                    Tax(0.00),
                ]
            ],
        },
        {
            "label": "case_08",
            "input": [
                [
                    Operation("buy", 10.00, 10000),
                    Operation("sell", 50.00, 10000),
                    Operation("buy", 20.00, 10000),
                    Operation("sell", 50.00, 10000),
                ]
            ],
            "output": [
                [
                    Tax(0.00),
                    Tax(80000.00),
                    Tax(0.00),
                    Tax(60000.00),
                ]
            ],
        },
        {
            "label": "case_09",
            "input": [
                [
                    Operation("buy", 10.00, 100),
                    Operation("sell", 15.00, 50),
                    Operation("sell", 15.00, 50),
                ],
                [
                    Operation("buy", 10.00, 10000),
                    Operation("sell", 20.00, 5000),
                    Operation("sell", 5.00, 5000),
                ],
            ],
            "output": [
                [Tax(0.00), Tax(0.00), Tax(0.00)],
                [Tax(0.00), Tax(10000.00), Tax(0.00)],
            ],
        },
        {
            "label": "case_10",
            "input": [
                [
                    Operation("buy", 10.00, 10000),
                    Operation("sell", 5.00, 5000),
                    Operation("sell", 20.00, 3000),
                ],
                [
                    Operation("buy", 10.00, 10000),
                    Operation("buy", 25.00, 5000),
                    Operation("sell", 15.00, 10000),
                ],
                [
                    Operation("buy", 10.00, 10000),
                    Operation("buy", 25.00, 5000),
                    Operation("sell", 15.00, 10000),
                    Operation("sell", 25.00, 5000),
                ],
                [
                    Operation("buy", 10.00, 10000),
                    Operation("sell", 2.00, 5000),
                    Operation("sell", 20.00, 2000),
                    Operation("sell", 20.00, 2000),
                    Operation("sell", 25.00, 1000),
                ],
            ],
            "output": [
                [Tax(0.00), Tax(0.00), Tax(1000.00)],
                [Tax(0.00), Tax(0.00), Tax(0.00)],
                [Tax(0.00), Tax(0.00), Tax(0.00), Tax(10000.00)],
                [
                    Tax(0.00),
                    Tax(0.00),
                    Tax(0.00),
                    Tax(0.00),
                    Tax(3000.00),
                ],
            ],
        },
    ]
