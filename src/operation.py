from dataclasses import dataclass


@dataclass
class Operation:
    """Represents an unitary operation (buy or sell)."""

    operation: str
    unit_cost: float
    quantity: int

    @property
    def total_value(self) -> float:
        return self.unit_cost * self.quantity

    def __eq__(self, other) -> bool:
        return all(
            [
                self.operation == other.operation,
                self.unit_cost == other.unit_cost,
                self.quantity == other.quantity,
            ]
        )
