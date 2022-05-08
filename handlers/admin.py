from cgitb import text
from aiogram.dispatcher import FSMContext #будем указывать что этот хендлер используется в машине состояний
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ID = None #изначально значение 0

class FSMAdmin(StatesGroup):
    name = State() #State - обозначаем, что это состояние бота
    lastname = State()
    # description = State()
    # price = State()


#Получаем ID текущего модератора
# @dp.message_handler(commands=['moderator'], is_chat_admin=True)#moderator-команда активации
async def make_change_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id,'Привет, модератор! 👋🏻 \r\n' 
                                                'Выбери необходимое действие.', reply_markup=admin_kb.button_case_admin)
    await message.delete()

#Начало диалога загрузки нового пункта меню
# @dp.message_handler(commands='Загрузить', state=None)#сначала бот не в режиме машиносостояний
# async def cm_start(message : types.Message):
#     if message.from_user.id == ID:
#         await FSMAdmin.photo.set() #переходит в режим машиносостояний, состояние ожидания на вопрос
#         await message.reply('Загрузи фото')

async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.name.set()#переводим бота в ожидание next state
        await message.reply('Введи имя:')   

#Выход из состояний
# @dp.message_handler(state="*", commands='Отмена')#state="*"-любое состояние,название
# @dp.message_handler(Text(equals='Отмена',ignore_case=True), state="*")#ignore_case-в любом регистре
async def cancel_handler(message: types.Message, state:FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()#получаем состояние бота
        if current_state is None:#если бот ни в одном состоянии
            return
        await state.finish()#закрываем машинусостояний
        await message.reply('OK')

#Ловим первый ответ и пишем в словарь
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo) #state=FSMAdmin.photo-бот понимает, что сюда попадет 1st ответ от user
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data: #открываем словарь
            data['name'] = message.text #записываем значение, получаем id фото
        await FSMAdmin.next()#переводим бота в ожидание next state
        await message.reply("Введи фамилию:")

#Ловим второй ответ
# @dp.message_handler(state=FSMAdmin.name) #
# async def load_name(message: types.Message, state: FSMContext):
#     if message.from_user.id == ID:
#         async with state.proxy() as data: #открываем словарь
#             data['lastname'] = message.text #записываем значение
#         await FSMAdmin.next()#переводим бота в ожидание next state
#         await message.reply("Введи описание")    

#Ловим третий ответ
# @dp.message_handler(state=FSMAdmin.description) #
# async def load_description(message: types.Message, state: FSMContext):
#     if message.from_user.id == ID:
#         async with state.proxy() as data: #открываем словарь
#             data['description'] = message.text #записываем значение
#         await FSMAdmin.next()#переводим бота в ожидание next state
#         await message.reply("Теперь укажи цену")  

#Ловим последний ответ
# @dp.message_handler(state=FSMAdmin.price) 
async def load_lastname(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data: #открываем словарь
            data['lastname'] = message.text #записываем значение
        await sqlite_db.sql_add_command(state)
        await state.finish()#бот выходит из машиносостояний и очищает словарь

#q хендлер для ответа
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))#если событие начинается на 'del '
async def del_callback_run(callback_query: types.CallbackQuery):#callback_query-название параметра
        await sqlite_db.sql_delete_command(callback_query.data.replace("del ", ""))#команда удаления
        await callback_query.answer(text=f'Сотрудник {callback_query.data.replace("del ", "")} удален.', show_alert=True)#отправляем, что запрос выполнен

@dp.message_handler(commands='Удалить')
async def delete_item(message:types.Message):
    read = await sqlite_db.sql_read2()#читаем данные (sqlite_db)
    keyboard = types.InlineKeyboardMarkup()
    if message.from_user.id == ID:
        for ret in read:#по получившемуся списку проходим
            # await bot.send_message(message.from_user.id, f'{ret[0]}\nИмя: {ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')
            keyboard.add(types.InlineKeyboardButton( f'{ret[0]} {ret[-1]}', callback_data=f'del {ret[1]}'))
        await bot.send_message(message.from_user.id, text='Выберите сотрудника для удаления:', reply_markup=keyboard)
                # add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))#по названию через callback_data отправляем в бд запрос на удаление


#Регистрируем хендлеры
def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='Отмена')
    dp.register_message_handler(cancel_handler, Text(equals='Отмена',ignore_case=True), state="*") 
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    # dp.register_message_handler(load_name, state=FSMAdmin.name)
    # dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_lastname, state=FSMAdmin.lastname)   
    dp.register_message_handler(make_change_command, commands=['moderator'], is_chat_admin=True )
    # dp.register_message_handler(del_callback_run, lambda x: x.data and x.data.startwith('del ')) 
    # dp.register_message_handler(delete_item, commands=['Удалить'])  

