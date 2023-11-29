from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher, executor, types

from api import bot_token, signup, get_usd_rate, update_usd_rate
from api import notification_subscription, get_notification_list
from api import get_user_requests, get_user_data


bot = Bot(bot_token)
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler(timezone='Europe/Moscow')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    chat_id = message.chat.id
    username = message.chat.username
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    msg = signup(chat_id, username, first_name, last_name)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Узнать текущий курс доллара'))
    markup.add(types.KeyboardButton('Показать историю запросов'))
    markup.add(types.KeyboardButton('Подписаться/отписаться на оповещение'))
    markup.add(types.KeyboardButton('Получить данные обо мне'))
    await message.answer(msg, reply_markup=markup)


@dp.message_handler(commands=['rate'])
async def rate(message: types.Message):
    msg = get_usd_rate(message.chat.id)
    await message.answer(msg)


@dp.message_handler(commands=['requests'])
async def rate(message: types.Message):
    msg = get_user_requests(message.chat.id)
    await message.answer(msg)


@dp.message_handler(commands=['me'])
async def rate(message: types.Message):
    msg = get_user_data(message.chat.id)
    await message.answer(msg)


@dp.message_handler(commands=['subscription'])
async def rate(message: types.Message):
    msg = notification_subscription(message.chat.id)
    await message.answer(msg)


@dp.message_handler(content_types=['text'])
async def get_text_messages(message):
    if message.text == 'Узнать текущий курс доллара':
        msg = get_usd_rate(message.chat.id)
        await message.answer(msg)
    elif message.text == 'Показать историю запросов':
        msg = get_user_requests(message.chat.id)
        await message.answer(msg)
    elif message.text == 'Подписаться/отписаться на оповещение':
        msg = notification_subscription(message.chat.id)
        await message.answer(msg)
    elif message.text == 'Получить данные обо мне':
        msg = get_user_data(message.chat.id)
        await message.answer(msg)


async def notification():
    notification_list, msg = get_notification_list()
    for chat_id in notification_list:
        await bot.send_message(chat_id, msg)


scheduler.add_job(update_usd_rate, 'cron',day_of_week='mon-fri',
                  hour=9, minute=58)
scheduler.add_job(notification, 'cron', day_of_week='mon-fri',
                  hour=10, minute=0)
scheduler.start()
executor.start_polling(dp)
