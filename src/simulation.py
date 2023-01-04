from dataclasses import dataclass

from src.constants import (
    MIN_TAXED_OPERATION_VALUE,
    TAX_PERCENTAGE,
)
from src.operation import Operation
from src.tax import Tax


@dataclass
class Simulation:
    """Keeps a simulation state, allowing buy and sell operations."""

    total_stocks: int = 0
    weighted_average: float = 0.0
    loss: float = 0.0

    def buy(self, operation: Operation) -> Tax:
        """Apply a buy operation and return corresponding tax (always zero)."""

        # buying operations required weighted_average to be updated
        # before changing the total_stocks
        self.weighted_average = Simulation.calculate_weighted_average(
            self.total_stocks,
            self.weighted_average,
            operation.quantity,
            operation.unit_cost,
        )
        self.total_stocks += operation.quantity
        return Tax(0.0)

    def sell(self, operation: Operation) -> Tax:
        """Apply a sell operation and return corresponding tax."""

        tax = 0.0
        self.total_stocks -= operation.quantity

        if (
            operation.total_value > MIN_TAXED_OPERATION_VALUE
            and operation.unit_cost > self.weighted_average
        ):
            profit = operation.quantity * (operation.unit_cost - self.weighted_average)

            # the taxable profit must be reduced from previous losses
            profit_adjusted = max(0.0, profit - self.loss)

            # the loss must be reduced after a taxable and profitable operation
            self.loss = max(0.0, self.loss - profit)

            # if any profit is left, constant tax percentage is applied
            tax = profit_adjusted * TAX_PERCENTAGE

        elif operation.unit_cost <= self.weighted_average:
            self.loss += operation.quantity * (
                self.weighted_average - operation.unit_cost
            )

        return Simulation.make_tax(tax)

    @staticmethod
    def calculate_weighted_average(
        current_stocks: int,
        current_weighted_average: float,
        new_stocks: int,
        buy_price: float,
    ) -> float:
        """Calculates the weighted average price."""
        current_amount = current_stocks * current_weighted_average
        new_amount = new_stocks * buy_price
        new_weighted_average = (current_amount + new_amount) / (
            current_stocks + new_stocks
        )
        return round(new_weighted_average, 2)

    @staticmethod
    def make_tax(tax: float) -> Tax:
        """Creates a Tax object from a float and rounds to 2 decimal digits."""
        return Tax(round(tax, 2))
