from aiogram import Dispatcher, types
from create_bot import dp, bot
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#главная команда
# @dp.message_handler(commands=['start','help'])
async def commands_start(message : types.Message):
    try:#пример ответа в чате и переход в ЛС, я не использую
        await bot.send_message(message.from_user.id, 'Добро пожаловать, тупица,{0.first_name} 👋🏻 \r\n'
                     'Здесь ты можешь поделиться своим мнением о качестве работы TS в три клика.\r\n'
                     'А мы обязательно прислушаемся к тебе и будем лучше в будущем ❤️'.format(message.from_user),
                     parse_mode='html', reply_markup=kb_client) #reply_markup-передаем клаву
        # await message.delete() #шото удаляет
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему: \nhttps://t.me/Technical_SupportLC_Bot')

#вторая команда
# @dp.message_handler(commands=['Оставить оценку'])
# async def pizza_open_command(message : types.Message):
#     await bot.send_message(message.from_user.id,'вс-чт,пт-пн')

#третья команда
# @dp.message_handler(commands=['Расположение'])
# async def pizza_place_command(message : types.Message):
#     await bot.send_message(message.from_user.id,'добролюбова') #reply_markup=ReplyKeyboardRemove()-клава удаляется+надо удалить one_time_keyboard=True из kb


# @dp.message_handler(commands=['Меню'])

async def checkstaff(message: types.Message):
    # global id_staff
    read = await sqlite_db.sql_read2()
    keyboard = types.InlineKeyboardMarkup()
    for ret in read:
        keyboard.add(types.InlineKeyboardButton( f'{ret[0]} {ret[-1]}', callback_data = 'fl_stuff'))
        # id_staff = f'{ret[-1]}'
    await bot.send_message(message.from_user.id,text='Пожалуйста, выберите сотрудника:', reply_markup=keyboard)    
# async def delete_item(message:types.Message):
#     if message.from_user.id == ID:
#         read = await sqlite_db.sql_read2()#читаем данные (sqlite_db)
#         for ret in read:#по получившемуся списку проходим
#             # await bot.send_message(message.from_user.id, f'{ret[0]}\nИмя: {ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')
#             await bot.send_message(message.from_user.id, text='Сотрудник', reply_markup=InlineKeyboardMarkup().\
#                 # add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))#по названию через callback_data отправляем в бд запрос на удаление
#                  add(InlineKeyboardButton( f'{ret[0]} {ret[-1]}', callback_data=f'del {ret[1]}')))        


# other.register_handlers_other(dp)
   #ПРИМЕР ОТВЕТА НА КОНКРЕТНОЕ СМС
    #  if message.text == 'Привет':
    #      await message.answer('И тебе привет!')

    #await message.answer(message.text)#await-подождать, пока не появится свободное место
    #await message.reply(message.text)#"ответить" на смс
    # await bot.send_message(message.from_user.id,message.text )#"ответить" в лс

#команды для регистрации хендлера для бота и передать при помощи этой функции все хендлеры в Technical_SupportLC_Bot
def register_handlers_client(dp : Dispatcher):
    #регистрирует хендлеры для бота и отправка в основной файл
    dp.register_message_handler(commands_start, commands=['start','help'])
    # dp.register_message_handler(pizza_open_command, commands=['Оставить_оценку'])
    # dp.register_message_handler(pizza_place_command, commands=['Расположение'])
    dp.register_message_handler(checkstaff, commands=['Оставить_оценку'])