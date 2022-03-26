from aiogram import types, Dispatcher
from create_bot import dp
import json, string #чтобы могли прочинать токен из переменных среды окружения


# @dp.message_handler()#событие что кто-то пишет
# async def echo_send(message : types.Message): #aiogram - ассинхронная библиотека (сюда попадают любые текст.смс от user)
#     #фильтр
#     if {i.lower().translate(str.maketrans('','', string.punctuation)) for i in message.text.split(' ')}\
#         .intersection(set(json.load(open('cenz.json')))) != set():
#         await message.reply('Маты запрещены!')
#         await message.delete()

#команды для регистрации хендлера для бота и передать при помощи этой функции все хендлеры в Technical_SupportLC_Bot
# def register_handlers_other(dp : Dispatcher):
#     #регистрирует хендлеры для бота
#     dp.register_message_handler(echo_send)