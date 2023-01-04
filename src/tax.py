from dataclasses import dataclass
from json import dumps


@dataclass
class Tax:
    tax: float

    def __eq__(self, other) -> bool:
        return self.tax == other.tax
