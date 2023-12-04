from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher, executor, types

from api import bot_token, signup, update_usd_rate, get_usd_rate
from api import get_user_data, get_user_requests
from api import change_user_notification_status, get_notified_list


bot = Bot(bot_token)
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler(timezone='Europe/Moscow')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    chat_id = message.chat.id
    firstname = message.chat.first_name
    lastname = message.chat.last_name
    username = message.chat.username
    msg = signup(chat_id, firstname, lastname, username)

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                       resize_keyboard=True)
    markup.add(types.KeyboardButton('Узнать текущий курс доллара'))
    markup.add(types.KeyboardButton('Показать историю запросов'))
    markup.add(types.KeyboardButton('Подписаться/отписаться на оповещение'))
    markup.add(types.KeyboardButton('Получить данные обо мне'))

    await message.answer(msg, parse_mode='HTML', reply_markup=markup)


@dp.message_handler(content_types=['text'])
async def get_text_messages(message):
    if message.text == 'Узнать текущий курс доллара':
        msg, notification_status = get_usd_rate(message.chat.id)
        markup = types.InlineKeyboardMarkup(resize_keyboard=True)
        if not notification_status:
            markup.add(types.InlineKeyboardButton('Подписаться на оповещение',
                                                  callback_data='subscription'))        
        markup.add(types.InlineKeyboardButton('Показать историю запросов',
                                              callback_data='requests'))
        await message.answer(msg, parse_mode='HTML', reply_markup=markup)

    elif message.text == 'Показать историю запросов':
        msg = get_user_requests(message.chat.id)
        await message.answer(msg, parse_mode='HTML')

    elif message.text == 'Подписаться/отписаться на оповещение':
        msg = change_user_notification_status(message.chat.id)
        await message.answer(msg, parse_mode='HTML')

    elif message.text == 'Получить данные обо мне':
        msg = get_user_data(message.chat.id)
        await message.answer(msg, parse_mode='HTML')


@dp.callback_query_handler()
async def callback_answer(callback):
    if callback.data == 'subscription':
        msg = change_user_notification_status(callback.message.chat.id)
        await callback.message.answer(msg, parse_mode='HTML')
    elif callback.data == 'requests':
        msg = get_user_requests(callback.message.chat.id)
        await callback.message.answer(msg, parse_mode='HTML')


async def notification():
    notified_list, msg = get_notified_list()
    for chat_id in notified_list:
        await bot.send_message(chat_id, msg, parse_mode='HTML')


scheduler.add_job(update_usd_rate, 'cron', day_of_week='mon-sat',
                  hour=9, minute=58)
scheduler.add_job(notification, 'cron', day_of_week='mon-sat',
                  hour=10, minute=0)
scheduler.start()

executor.start_polling(dp)
