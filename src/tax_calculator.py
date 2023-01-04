from typing import List

from src.operation import Operation
from src.simulation import Simulation
from src.tax import Tax


class TaxCalculator:
    @staticmethod
    def calculate(operations: List[Operation]) -> List[Tax]:
        """Calculate taxes for each operation in a list."""
        simulation = Simulation(0, 0.0, 0.0)
        result = []
        # operations must be computed sequentially
        for operation in operations:
            if operation.operation == "buy":
                result.append(simulation.buy(operation))
            elif operation.operation == "sell":
                result.append(simulation.sell(operation))
        return result
