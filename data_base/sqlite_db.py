import sqlite3 as sq#встроенная бд, использует 1 файл
from create_bot import dp, bot
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def sql_start():#создание, подключение
    global base, cur
    base = sq.connect('techsup.db')#подключение к файлу бд, если его нет, то он создасться
    cur = base.cursor()#поиск, встраивание и выборка из бд
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS staff(name TEXT, lastname TEXT PRIMARY KEY)')#IF NOT EXISTS-если такой не сущ-ет
    base.execute('CREATE TABLE IF NOT EXISTS note(id INTEGER PRIMARY KEY AUTOINCREMENT, lastname TEXT, note TEXT, id_user TEXT)')
    base.commit()#записать

async def sql_add_command(state):#функция изменения бд
    async with state.proxy() as data:#открываем словарь
        cur.execute('INSERT INTO staff VALUES (?, ?)', tuple(data.values()))#?-шифруем значения
        base.commit()

async def sql_add_note_command(state):#функция изменения бд
    async with state.proxy() as data:#открываем словарь
        cur.execute('INSERT INTO note(lastname, note, id_user) VALUES (?, ?, ?)', tuple(data.values()))#?-шифруем значения
        base.commit()

async def sql_read(message:types.Message):#получаем событие смс, когда нажимают на кнопку "Меню"
    for ret in cur.execute('SELECT * FROM staff').fetchall():#выгружает в виде списка и получаем в переменную ret
        # markup = InlineKeyboardMarkup()
        # markup.row_width = 2
        # ret = types.InlineKeyboardButton(f'{ret[0]}\nимя: {ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')
        # markup.add(InlineKeyboardButton(ret, callback_data="cb_yes"))
        # # await bot.send_message(message.from_user.id,"Пожалуйста, выберите сотрудника",reply_markup=markup)
        await bot.send_message(message.from_user.id, f'{ret[0]} {ret[-1]}')#0-фото, 1-название и тд

async def sql_read2():
    return cur.execute('SELECT * FROM staff').fetchall()#прочитать выборку из таблицы и возвращаем в admin.py delete_item

async def sql_read_department():
    return cur.execute('SELECT * FROM department').fetchall()    

async def sql_delete_command(data):#по названию
    cur.execute('DELETE FROM staff WHERE lastname == ?', (data,))
    base.commit()

