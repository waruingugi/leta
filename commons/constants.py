from enum import Enum

# Cut from product price that supplier gets
SUPPLIER_SHARE: float = 0.7


# Number of best selling products to show in
# GET /analytics/best-selling-products/
BEST_SELLING_PRODUCTS_LIMIT: int = 50


# Statuses for order model
class OrderStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


# Discount Types
class DiscountType(str, Enum):
    FLAT = "FLAT"


# Customer Membership Levels
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
