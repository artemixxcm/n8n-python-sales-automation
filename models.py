from dataclasses import dataclass

@dataclass
class Sale:
    product: str
    category: str
    value: float
    quantity: int
    date: str
    id: int = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "product": self.product,
            "category": self.category,
            "value": self.value,
            "quantity": self.quantity,
            "date": self.date
        }