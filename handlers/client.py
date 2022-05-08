from aiogram import Dispatcher, types
from create_bot import dp, bot
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re
from aiogram.dispatcher import FSMContext #будем указывать что этот хендлер используется в машине состояний
from aiogram.dispatcher.filters.state import State, StatesGroup

 #State - обозначаем, что это состояние бота
class FSMAdmin(StatesGroup):
    name = State() #State - обозначаем, что это состояние бота
    lastname = State()
    id_user = State()
    # staff_name = State()
#главная команда
# @dp.message_handler(commands=['start','help'])
async def commands_start(message : types.Message):
    try:#пример ответа в чате и переход в ЛС, я не использую
        await bot.send_message(message.from_user.id, 'Добро пожаловать,{0.first_name} 👋🏻 \r\n'
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




# @dp.message_handler(state=FSMAdmin.staff_name) 
# async def set_staff_name(message: types.Message, state: FSMContext):
#     async with state.proxy() as data: #открываем словарь
#         data['staff_name'] = message.text #записываем значение
#     await sqlite_db.sql_add_note_command(state)
#     await state.finish()
#     await message.reply('Спасибо!\r\n'
#                         'Будем рады видеть вас снова ❤ ')

# @dp.message_handler(state=FSMAdmin.department) 
# async def set_department(message: types.Message, state: FSMContext):
#     async with state.proxy() as data: #открываем словарь
#         data['department'] = message.text #записываем значение, получаем id фото
#     await FSMAdmin.next()#переводим бота в ожидание next state
#     await message.reply('Осталось совсем чуть-чуть!\r\n'
#         '\r\n'
#         'Подскажите своё имя и фамилию')

# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('set_department '))
# async def set_department(callback_query: types.CallbackQuery):
#     # global id_staff
#     read = await sqlite_db.sql_read_department()
#     keyboard = types.InlineKeyboardMarkup()
#     for ret in read:
#         keyboard.add(types.InlineKeyboardButton( f'{ret[-1]}', callback_data = f'set_department {ret[-1]}'))
#     await bot.send_message(callback_query.from_user.id,text='Выберите свой отдел:', reply_markup=keyboard)


#выставляем оценку сотруднику
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('set_note '))#если событие начинается на 'del '
async def set_note(callback_query: types.CallbackQuery, state: FSMContext):#callback_query-название параметра
    note_result = re.search(r'\d', callback_query.data)
    note = note_result.group(0)
    last_name = callback_query.data.replace(f"set_note {note} ", "")
    id_user = callback_query.from_user.id
    # await FSMAdmin.name.set()
    async with state.proxy() as data:
        data['lastname'] = last_name
        data['note'] = note
        data['id_user'] = id_user
    await bot.send_message(callback_query.from_user.id, text=f'Спасибо за обратную связь!')
    # await set_department(callback_query)    
    await sqlite_db.sql_add_note_command(state)
    await state.finish()
    # await FSMAdmin.next()
    # await message.reply('Спасибо за обратную связь!\r\n'
    #     '\r\n' 
    #     'Пожалуйста, оставите немного информации о себе.')
    # await state.finish()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('set_staff '))#если событие начинается на 'del '
async def set_staff(callback_query: types.CallbackQuery):#callback_query-название параметра
        keyboard = types.InlineKeyboardMarkup()
        for i in range(1,4):
            keyboard.add(types.InlineKeyboardButton(f'{i}', callback_data=f'set_note {i} {callback_query.data.replace("set_staff ", "")}'))
        await bot.send_message(callback_query.from_user.id, text=f'Сотрудник {callback_query.data.replace("set_staff ", "")} выбран.\n'
        '\r\n'
        'Пожалуйста, отправьте свою оценку от 1 до 3, где:\r\n'
        '\r\n'
        '1 - оценю работу ниже ожиданий\r\n'
        '2 - оценю работу в рамках ожиданий\r\n'
        '3 - оценю работу в выше ожиданий', reply_markup=keyboard)#отправляем, что запрос выполнен


@dp.message_handler(commands='Оставить_оценку')
async def checkstaff(message: types.Message):
    # global id_staff
    read = await sqlite_db.sql_read2()
    keyboard = types.InlineKeyboardMarkup()
    for ret in read:
        keyboard.add(types.InlineKeyboardButton( f'{ret[0]} {ret[-1]}', callback_data = f'set_staff {ret[1]}'))
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
    # dp.register_message_handler(checkstaff, commands=['Оставить_оценку'])