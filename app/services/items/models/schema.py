from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, validates

from db.base import Base
from services.items.models.enum_models import ItemCategory


class Item(Base):

    __tablename__ = "Item"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[Optional[str]]
    category: Mapped[str]
    quantity: Mapped[int]
    price: Mapped[float]

    @validates("category")
    def validate_category(self, key, category):
        if category not in ItemCategory:
            raise ValueError(f"Invalid category: {category}. Available values {[item.value for item in ItemCategory]}")
        return category

    @validates("quantity")
    def validate_quantity(self, key, quantity):
        if quantity < 0:
            raise ValueError(f"Invalid quantity value: {quantity}. Quantity cannot be less than 0")
        return quantity

    @validates("price")
    def validate_price(self, key, price):
        if price < 0:
            raise ValueError(f"Invalid price value: {price}. Price cannot be less than 0")
        return price
