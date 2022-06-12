from email.mime import message
from aiogram import Dispatcher, types
from create_bot import dp, bot
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re
from aiogram.dispatcher import FSMContext #будем указывать что этот хендлер используется в машине состояний
from aiogram.dispatcher.filters.state import State, StatesGroup

global people_dict
people_dict = {}

class FSMAdmin(StatesGroup):
    name = State() #State - обозначаем, что это состояние бота
    lastname = State()
    # id_user = State()

class FSMclient(StatesGroup):
    write = State() #State - обозначаем, что это состояние бота
    name = State()
    lastname = State()


#главная команда
@dp.message_handler(commands=['start','help']) 
async def commands_start(message : types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Добро пожаловать,{0.first_name} 👋🏻 \r\n'
                     'Здесь ты можешь поделиться своим мнением о качестве работы TS в три клика.\r\n'
                     'А мы обязательно прислушаемся к тебе и будем лучше в будущем ❤️'.format(message.from_user),
                     parse_mode='html', reply_markup=kb_client) #reply_markup-передаем клаву
        # await message.delete() #шото удаляет
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему: \nhttps://t.me/Technical_SupportLC_Bot')


@dp.message_handler(commands='Оставить_оценку')
async def checkstaff(message: types.Message):
    read = await sqlite_db.sql_read_users_ts_command()
    keyboard = types.InlineKeyboardMarkup()
    for ret in read:
        keyboard.add(types.InlineKeyboardButton( f'{ret[1]} {ret[2]}', callback_data = f'set_staff {ret[2]}'))
    await bot.send_message(message.from_user.id,text='Пожалуйста, выберите сотрудника:', reply_markup=keyboard)  


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('set_staff '))
async def set_staff(callback_query: types.CallbackQuery):
        keyboard = types.InlineKeyboardMarkup()
        for i in range(1,6):
            keyboard.add(types.InlineKeyboardButton(f'{i}', callback_data=f'set_note {i} {callback_query.data.replace("set_staff ", "")}'))
        await bot.send_message(callback_query.from_user.id, text=f'Сотрудник {callback_query.data.replace("set_staff ", "")} выбран.\n'
        '\r\n'
        'Пожалуйста, отправьте свою оценку от 1 до 5, где:\r\n'
        '\r\n'
        '1 - оцениваю работу ниже ожиданий\r\n'
        '5 - оцениваю работу выше ожиданий', reply_markup=keyboard)


#выставляем оценку сотруднику
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('set_note '))#если событие начинается на 'set_note '
async def set_note(callback_query: types.CallbackQuery, state: FSMContext):#callback_query-название параметра
    #await bot.send_message(callback_query.from_user.id, text="Я работаю")
    note_result = re.search(r'\d', callback_query.data)
    note = note_result.group(0)
    last_name = callback_query.data.replace(f"set_note {note} ", "")
    # id_user = callback_query.from_user.id
    # await FSMAdmin.name.set()
    async with state.proxy() as data:
        data['note'] = note
        data['id_note'] = await sqlite_db.sql_add_note_command(note)
        data['id_recipient'] = await sqlite_db.sql_get_id_by_lastname(last_name)
        await sqlite_db.sql_add_note_recipient_command(data)
    if int(note) < 5:
        # ввод комментария, запись коммента, потом вызов записи ифномрации о клиенте
        
        pass
    else:
        await bot.send_message(callback_query.from_user.id, text = 'Спасибо за обратную связь!\nОставьте, пожалуйста, немного информации о себе:') # вызов записи инфы о клиенте
        #await state.finish()
        await select_department(callback_query)
  

  

#выбор отдела сотрудником
async def select_department(callback_query: types.CallbackQuery):
    #await FSMclient.department.set()#переводим бота в ожидание next state
    read = await sqlite_db.sql_read_department()
    keyboard = types.InlineKeyboardMarkup()
    for ret in read:
        if ret[1] != 'Техническая поддержка':
            keyboard.add(types.InlineKeyboardButton( f'{ret[1]}', callback_data = f'set_department {ret[0]}'))
    await bot.send_message(callback_query.from_user.id, text='Выберите свой отдел:', reply_markup=keyboard)
    # await FSMclient.name.set()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('set_department ')) 
async def set_department(callback_query: types.CallbackQuery, state: FSMclient):
    global id_department
    id_department = callback_query.data.replace("set_department ", "")
    await bot.send_message(callback_query.from_user.id, text=f'Я работаю в {id_department}')
    await FSMclient.name.set()
    await bot.send_message(callback_query.from_user.id, text='Введите имя:')

@dp.message_handler(state=FSMclient.name)
async def set_name(message: types.Message, state: FSMclient):
    global name
    name = message.text
    await FSMclient.lastname.set()
    await message.answer(text = 'Введите свою фамилию:')

@dp.message_handler(state=FSMclient.lastname)
async def set_lastname(message: types.Message, state: FSMclient):
    global lastname, id_department, name
    lastname = message.text
    await state.finish()
    await message.answer(text = f'Записано: {id_department, name, lastname}')














    # @dp.message_handler(state=FSMAdmin.department) 
# async def set_department(message: types.Message, state: FSMContext):
#     async with state.proxy() as data: #открываем словарь
#         data['department'] = message.text #записываем значение, получаем id фото
#     await FSMAdmin.next()#переводим бота в ожидание next state
#     await message.reply('Осталось совсем чуть-чуть!\r\n'
#         '\r\n'
#         'Подскажите своё имя и фамилию')






#вторая команда
# @dp.message_handler(commands=['Оставить оценку'])
# async def pizza_open_command(message : types.Message):
#     await bot.send_message(message.from_user.id,'вс-чт,пт-пн')

#третья команда
# @dp.message_handler(commands=['Расположение'])
# async def pizza_place_command(message : types.Message):
#     await bot.send_message(message.from_user.id,'добролюбова') #reply_markup=ReplyKeyboardRemove()-клава удаляется+надо удалить one_time_keyboard=True из kb

# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('set_department '))
# async def set_department(callback_query: types.CallbackQuery):
#     # global id_staff
#     read = await sqlite_db.sql_read_department()
#     keyboard = types.InlineKeyboardMarkup()
#     for ret in read:
#         keyboard.add(types.InlineKeyboardButton( f'{ret[-1]}', callback_data = f'set_department {ret[-1]}'))
#     await bot.send_message(callback_query.from_user.id,text='Выберите свой отдел:', reply_markup=keyboard)
  
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