from pydantic import BaseModel, Field


class StockBalance(BaseModel):
    warehouse_name: str = Field(nullable=False, description="Warehouse name")
    name: str = Field(nullable=False, description="Product name")
    artikul: str = Field(nullable=False, description="Artikul")
    quantity: int = Field(nullable=False, description="Quantity")
