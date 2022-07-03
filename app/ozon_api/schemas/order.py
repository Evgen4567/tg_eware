from datetime import datetime

from pydantic import BaseModel, Field, condecimal


class Order(BaseModel):
    market_id: str = Field(nullable=False, description="ID from Market")
    status: str = Field(nullable=False, description="Status of order")
    city: str = Field(nullable=False, description="Delivery city")
    warehouse: str = Field(nullable=False, description="Warehouse name")
    order_datetime: datetime = Field(nullable=False, description="Order datetime")
    name: str = Field(nullable=False, description="Name")
    artikul: str = Field(nullable=False, description="Artikul")
    quantity: int = Field(nullable=False, description="Quantity")
    sell_price: condecimal(max_digits=5, decimal_places=2) = Field(default=0, description="Sell price")
