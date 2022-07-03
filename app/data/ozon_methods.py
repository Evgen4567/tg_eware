from typing import List

from ozon_api import get_posting_list, get_warehouses_stock, Posting
from ozon_api.schemas.order import Order
from ozon_api.schemas.warehouse import WarehousesStock
from ozon_api.schemas.stock_balance import StockBalance


def parse_orders_data(data: List[Posting]) -> List[Order]:
    result = []
    for posting in data:
        for product in posting.products:
            result.append(
                Order(
                    market_id=posting.posting_number,
                    status=posting.status,
                    city=posting.analytics_data.city,
                    warehouse=posting.analytics_data.warehouse_name,
                    order_datetime=posting.created_at,
                    name=product.name,
                    artikul=product.offer_id,
                    quantity=product.quantity,
                    price=product.price
                )
            )
    return result


def parse_warehouses_stock(data: WarehousesStock) -> List[StockBalance]:
    result = []
    for item in data.wh_items:
        wh_name = item.name
        for product in item.items:
            result.append(
                StockBalance(
                    warehouse_name=wh_name,
                    artikul=product.offer_id,
                    quantity=product.stock.for_sale,
                    name=product.title
                )
            )
    return result


def get_orders_data() -> List[Order]:
    result = []

    limit = 1000
    offset = 0
    response = get_posting_list(limit=limit, offset=offset)
    wet_orders = response['result']
    result.extend([Posting(**posting) for posting in wet_orders])
    while len(wet_orders) > 0:
        offset += len(wet_orders)
        response = get_posting_list(limit=limit, offset=offset)
        wet_orders = response['result']
        result.extend([Posting(**posting) for posting in wet_orders])

    return parse_orders_data(result)


def get_warehouses_data() -> List[StockBalance]:
    ozon_data = get_warehouses_stock()
    return parse_warehouses_stock(ozon_data)


if __name__ == '__main__':
    orders = get_orders_data()
    wh = get_warehouses_data()
    print(wh)
