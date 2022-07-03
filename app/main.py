from aiogram import executor
from aiogram.utils.executor import start_webhook

from bot import dp, bot
from config import logger, WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_PORT, WEBAPP_HOST


async def on_startup(dispatcher):
    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()


if __name__ == '__main__':
    logger.info('Start bot')
    # executor.start_polling(dp, skip_updates=True)

    # webserver settings
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )

