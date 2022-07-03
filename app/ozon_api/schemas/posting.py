from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel  # condecimal - float to double


class Product(BaseModel):
    sku: int
    name: str
    quantity: int
    offer_id: str
    price: str
    digital_codes: List[str]


class AnalyticsData(BaseModel):
    region: str
    city: str
    delivery_type: str
    is_premium: bool
    payment_type_group_name: str
    warehouse_id: int
    warehouse_name: str
    is_legal: bool


class Services(BaseModel):
    marketplace_service_item_fulfillment: float
    marketplace_service_item_pickup: float
    marketplace_service_item_dropoff_pvz: float
    marketplace_service_item_dropoff_sc: float
    marketplace_service_item_dropoff_ff: float
    marketplace_service_item_direct_flow_trans: float
    marketplace_service_item_return_flow_trans: float
    marketplace_service_item_deliv_to_customer: float
    marketplace_service_item_return_not_deliv_to_customer: float
    marketplace_service_item_return_part_goods_customer: float
    marketplace_service_item_return_after_deliv_to_customer: float


class FinancialProducts(BaseModel):
    commission_amount: float
    commission_percent: int
    payout: float
    product_id: int
    old_price: int
    price: int
    total_discount_value: int
    total_discount_percent: float
    actions: List[str]
    picking: Optional[str]
    quantity: int
    client_price: str
    item_services: Services


class FinancialData(BaseModel):
    products: List[FinancialProducts]
    posting_services: Services


class Posting(BaseModel):
    order_id: int
    order_number: str
    posting_number: str
    status: str
    cancel_reason_id: int
    created_at: datetime
    in_process_at: datetime
    additional_data: Optional[list]
    products: List[Product]
    analytics_data: AnalyticsData
    financial_data: FinancialData
