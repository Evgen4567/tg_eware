from typing import List


from pydantic import BaseModel


class Stock(BaseModel):
    not_for_sale: int
    loss: int
    for_sale: int


class Item(BaseModel):
    offer_id: str
    sku: int
    title: str
    category: str
    discounted: str
    barcode: str
    length: int
    width: int
    height: int
    volume: float
    stock: Stock


class Warehouse(BaseModel):
    id: str
    name: str
    items: List[Item]


class WarehousesStock(BaseModel):
    wh_items: List[Warehouse]
    timestamp: str
    total_items: List[Item]
