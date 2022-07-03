import os
from sys import stderr

from dotenv import load_dotenv
from loguru import logger


load_dotenv()
ENV = os.getenv("ENV", "dev")
logger.remove()
if ENV == "dev":
    logger.add(stderr, level="DEBUG")
else:
    logger.add("file.log", rotation="1 week", level="INFO")

OZON_API_HOST = "https://api-seller.ozon.ru"
OZON_HEADERS = {
    "accept": "application/json",
    "Client-Id": os.getenv("OZON_CLIENT_ID"),
    "Api-Key": os.getenv("OZON_API_KEY"),
    "Content-Type": "application/json"
}

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMINS_CHAT_ID = os.getenv("ADMINS").split(",")
ADMINS_CHAT_ID = [int(x) for x in ADMINS_CHAT_ID]


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
URAALA_ARTIKUL_PATH = f"{ROOT_DIR}/conv_artikuls_uraala.csv"

# webhook settings
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TELEGRAM_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)
