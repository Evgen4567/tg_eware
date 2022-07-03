from aiogram.contrib.middlewares.logging import LoggingMiddleware

from config import logger


class CustomLoggingMiddleware(LoggingMiddleware):

    def __init__(self, logger_name=__name__):
        super().__init__(logger=logger_name)
        self.logger = logger
