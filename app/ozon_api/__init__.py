import arrow

from datetime import datetime

from web_client import make_request
from config import OZON_API_HOST, OZON_HEADERS
from ozon_api.schemas.posting import Posting
from ozon_api.schemas.warehouse import WarehousesStock

from config import logger


def get_posting_list(
        direction: str = "asc", time_to: datetime = None, limit: int = 50, offset: int = 0
) -> dict:
    url = f'{OZON_API_HOST}/v2/posting/fbo/list'
    if time_to is None:
        time_to = arrow.utcnow().naive
    since = '2021-03-01T00:00:10.083Z'
    to = time_to.isoformat()[:-3] + 'Z'
    body = {
        "dir": direction,
        "filter": {
            "since": since,
            "to": to
        },
        "limit": limit,
        "offset": offset,
        "translit": True,
        "with": {
            "analytics_data": True,
            "financial_data": True
        }
    }
    logger.info(f'{body}')
    return make_request(method='POST', url=url, headers=OZON_HEADERS, json=body, timeout=30).json()


def get_posting(posting_number: str, analytics_data: bool = True, financial_data: bool = True) -> Posting:
    url = f'{OZON_API_HOST}/v2/posting/fbo/get'
    body = {
        "posting_number": posting_number,
        "with": {
            "analytics_data": analytics_data,
            "financial_data": financial_data
        }
    }
    logger.info(f'{body}')
    response = make_request(method='POST', url=url, headers=OZON_HEADERS, json=body).json()
    return Posting(**response['result'])


def get_warehouses_stock(limit: int = 1000000, offset: int = 0) -> WarehousesStock:
    url = f'{OZON_API_HOST}/v1/analytics/stock_on_warehouses'
    body = {"limit": limit, "offset": offset}
    logger.info(f'{body}')
    response = make_request(method='POST', url=url, headers=OZON_HEADERS, json=body).json()
    return WarehousesStock(**response)


if __name__ == '__main__':
    # warehouses_stock = get_warehouses_stock()
    posting_list = get_posting_list()

