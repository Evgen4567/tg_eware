from aiogram import executor

from bot import dp
from config import logger


if __name__ == '__main__':
    logger.info('Start bot')
    executor.start_polling(dp, skip_updates=True)
