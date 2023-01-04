import sys

from dataclasses import asdict
from json import dumps, loads
from typing import List

from src.operation import Operation
from src.tax_calculator import TaxCalculator


SimulationLine = List[Operation]


def parse_input(input_info: str) -> List[SimulationLine]:
    lines = [loads(line.strip()) for line in input_info.split("\n")]
    return [
        [
            Operation(
                operation["operation"], operation["unit-cost"], operation["quantity"]
            )
            for operation in line
        ]
        for line in lines
    ]


def main(input_string: str) -> None:
    simulations = parse_input(input_string)
    for operations in simulations:
        tax_applicable = TaxCalculator.calculate(operations)
        tax_applicable = [asdict(tax) for tax in tax_applicable]
        print(dumps(tax_applicable))


def entrypoint():
    input_string = sys.stdin.read()
    main(input_string)


if __name__ == "__main__":
    entrypoint()
