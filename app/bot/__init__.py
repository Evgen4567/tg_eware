import typing
import emoji
import pandas as pd

from collections import namedtuple
from json import loads
from io import BytesIO

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Filter

from bot.custom_logger import CustomLoggingMiddleware
from data.statistics import get_data_by_warehouse
from config import TELEGRAM_TOKEN, ADMINS_CHAT_ID, URAALA_ARTIKUL_PATH
from bot.navigation import get_element_from_path
from bot.static_menu import admin_menu
from config import logger


bot = Bot(token=TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(CustomLoggingMiddleware())
navigation_cb = CallbackData('button', 'path', 'name', 'action')


class Order(StatesGroup):
    name = State()
    file = State()


class IsAdmin(Filter):
    key = "is_admin"

    async def check(self, message: types.Message):
        return message.from_user.id in ADMINS_CHAT_ID


def get_keyboard(structure: namedtuple, path: list = None) -> types.InlineKeyboardMarkup:
    if path is None:
        path = []
    markup = types.InlineKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    for elem in structure.content:
        elem_path = path.copy()
        idx = structure.content.index(elem)
        elem_path.insert(0, idx)
        markup.add(
            types.InlineKeyboardButton(
                elem.name,
                callback_data=navigation_cb.new(path=elem_path, name=elem.name, action=elem.action)),
        )
    return markup


@dp.message_handler(IsAdmin(), commands='start')
async def cmd_start(message: types.Message):
    logger.info(message)
    await message.reply(
        emoji.emojize(f'Мое почтение... :person_bowing:', language='alias'), reply_markup=get_keyboard(admin_menu, [])
    )


@dp.callback_query_handler(IsAdmin(), navigation_cb.filter(action='navigation'))
async def query_navigation(query: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    name = callback_data['name']
    path = loads(callback_data['path'])
    element = get_element_from_path(path, admin_menu)
    await query.message.edit_text(name, reply_markup=get_keyboard(element, path))


@dp.callback_query_handler(IsAdmin(), navigation_cb.filter(action='get_prepared'))
async def query_back(query: types.CallbackQuery):
    in_memory_ekb = BytesIO()
    in_memory_msk = BytesIO()
    logger.info('start getting data by warehouse')
    data = get_data_by_warehouse()
    data.data_ekb.to_excel(in_memory_ekb, index=False)
    data.data_msk.to_excel(in_memory_msk, index=False)
    in_memory_ekb.seek(0, 0)
    in_memory_msk.seek(0, 0)
    await bot.send_document(query.from_user.id, document=('EKB.xlsx', in_memory_ekb.read()))
    await bot.send_document(query.from_user.id, document=('MSK.xlsx', in_memory_msk.read()))
    await bot.send_message(
        query.from_user.id,
        text=emoji.emojize(f'Данные для заказа появятся над этим сообщением 👆🏼', language='alias'),
        reply_markup=get_keyboard(admin_menu, [])
    )


@dp.callback_query_handler(IsAdmin(), navigation_cb.filter(action='format'))
async def query_order_ms(query: types.CallbackQuery, state: FSMContext, callback_data: typing.Dict[str, str]):
    await Order.name.set()
    async with state.proxy() as data:
        data['name'] = callback_data['name']

    await Order.next()
    await query.message.edit_text(f'Загрузи файл заказа 📩')


@dp.message_handler(IsAdmin(), content_types=["document"], state=Order.file)
async def process_file(message: types.Message, state: FSMContext):
    logger.info('start formatting document')
    await state.finish()
    in_memory = BytesIO()
    file_from_bot = await bot.get_file(message.document.file_id)
    await bot.download_file(file_from_bot.file_path, in_memory)
    in_memory.seek(0, 0)
    raw_df = pd.read_excel(in_memory.read())
    conv_artikuls = pd.read_csv(URAALA_ARTIKUL_PATH)
    df = conv_artikuls[['artikul', 'artikul_uraala']].join(
        raw_df.set_index('artikul'), on='artikul', how='outer'
    )
    await bot.send_message(
        message.from_user.id, text=emoji.emojize(f'Файл загружен. Меняю формат', language='alias')
    )

    logger.info('prepare and send ozon format')
    in_memory = BytesIO()
    to_ozon = df[['artikul', 'name', 'to_buy']]
    to_ozon.columns = ['артикул', 'имя (необязательно)', 'количество']
    to_ozon.to_excel(in_memory, index=False)
    in_memory.seek(0, 0)
    await bot.send_document(message.from_user.id, document=('to_ozon.xlsx', in_memory.read()))

    logger.info('prepare and send uraala format')
    in_memory = BytesIO()
    to_uraala = df[['name', 'artikul_uraala', 'to_buy']]
    to_uraala.columns = ['Наименование', 'Артикул', 'Количество']
    to_uraala.to_excel(in_memory, index=False)
    in_memory.seek(0, 0)
    await bot.send_document(message.from_user.id, document=('to_uraala.xlsx', in_memory.read()))

    await bot.send_message(
        message.from_user.id,
        emoji.emojize("Готов к новым поручениям! :man_mechanic:", language='alias'),
        reply_markup=get_keyboard(admin_menu, [])
    )


@dp.errors_handler(exception=MessageNotModified)
async def message_not_modified_handler(update, error):
    logger.error(f'{update=}\n{error=}')
    return True


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
