from enum import Enum

SUPPLIER_SHARE: float = 0.7


class MembershipLevel(str, Enum):
    BRONZE = "BRONZE"
    SILVER = "SILVER"
    GOLD = "GOLD"

    @property
    def discount(self) -> float:
        discounts = {
            "BRONZE": 0.0,  # 0% discount
            "SILVER": 5.0,  # 5% discount
            "GOLD": 10.0,  # 10% discount
        }
        return discounts[self.value]
