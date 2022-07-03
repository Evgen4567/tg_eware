import httpx

from config import logger


def make_request(**kwargs) -> httpx.Response:
    response = httpx.request(**kwargs)
    logger.info(f'{response.url} - {response.status_code}')
    return response
