from typing import List, Union

from src.operation import Operation
from src.simulation import Simulation
from src.tax import Tax
from src.tax_error import TaxError


class TaxCalculator:
    @staticmethod
    def calculate(operations: List[Operation]) -> List[Union[Tax, TaxError]]:
        """Calculate taxes for each operation in a list."""
        simulation = Simulation()
        result = []
        # operations must be computed sequentially
        for operation in operations:
            if operation.operation == "buy":
                result.append(simulation.buy(operation))
            elif operation.operation == "sell":
                result.append(simulation.sell(operation))
        return result
