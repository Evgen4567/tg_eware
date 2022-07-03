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
