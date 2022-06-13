import sqlite3 as sq#встроенная бд, использует 1 файл
from create_bot import dp, bot
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ------------------------------------------------------------------------------------------
# таблицы созданы - не нужно в Technical_SupportLC_Bot команда указана, пока пусть будет
def sql_start():#создание, подключение
    global base, cur
    base = sq.connect('techsup.db')#подключение к файлу бд, если его нет, то он создасться
    cur = base.cursor()#поиск, встраивание и выборка из бд
    if base:
        print('Data base connected OK!')       
    # base.execute('CREATE TABLE IF NOT EXISTS Users(id_users PRIMARY KEY AUTOINCREMENT, name TEXT, lastname TEXT)')#IF NOT EXISTS-если такой не сущ-ет 
    # base.execute('CREATE TABLE IF NOT EXISTS Note(id_note id_users PRIMARY KEY AUTOINCREMENT, note TEXT, comment TEXT)')
    base.commit()#записать
# ------------------------------------------------------------------------------------------
# ДОБАВЛЕНИЕ СОТРУДНИКА TS Users и UsersDepartment +++++++++++++++++++++
async def sql_add_users_command(state, message:types.Message):
    async with state.proxy() as data:#открываем словарь
        answer = cur.execute(f'SELECT COUNT(*) FROM Users u \
                            JOIN UsersDepartment ud ON u.id_users = ud.id_users\
                            WHERE lastname = "{data["lastname"]}" AND name = "{data["name"]}" AND id_department = 10')
        count = answer.fetchone()[0]
        if not count:
            cur.execute('INSERT INTO Users(name, lastname) VALUES (?, ?) ', tuple(data.values()))
            cur.execute(f'INSERT INTO UsersDepartment(id_users, id_department) VALUES ({cur.lastrowid}, 10)')
            base.commit()
            await bot.send_message(message.from_user.id, 'Сотрудник успешно добавлен')
        else:
            await bot.send_message(message.from_user.id, 'Такой сотрудник уже существует')
# ------------------------------------------------------------------------------------------
# УДАЛЕНИЕ Users TS ++++++++++++++++
async def sql_delete_TS_command(data):#по названию
    cur.execute('UPDATE Users SET deleted = 1 WHERE lastname == ?', (data,))
    base.commit()
# ------------------------------------------------------------------------------------------
# ДОБАВЛЕНИЕ ОЦЕНКИ в Note +++++++++++++++++++++++
async def sql_add_note_command(note):#функция изменения бд
    note = cur.execute(f"INSERT INTO Note('note') VALUES ({note})")
    base.commit()
    return note.lastrowid

# ------------------------------------------------------------------------------------------
# ДОБАВЛЕНИЕ комментария в Note ++++++++++++
async def sql_add_comment_note_command(comment_str: str, id_note: str):#функция изменения бд
    id_note = int(id_note)
    cur.execute("UPDATE Note SET comment = ? WHERE id_note = ?", (comment_str, id_note))
    base.commit()
# ------------------------------------------------------------------------------------------
# ДОБАВЛЕНИЕ автора в Users ++++++++++++++++++++
async def sql_add_all_users_command(name, lastname, id_department, message:types.Message):
    # async with state.proxy() as data:#открываем словарь
    answer = cur.execute(f'SELECT COUNT(*) FROM Users u \
                        JOIN UsersDepartment ud ON u.id_users = ud.id_users\
                        WHERE lastname = ? AND name = ?', (name, lastname))
    count = answer.fetchone()[0]
    if not count:
        cur.execute('INSERT INTO Users(name, lastname) VALUES (?, ?) ', (name, lastname))
        cur.execute(f'INSERT INTO UsersDepartment(id_users, id_department) VALUES ({cur.lastrowid}, {id_department})')
        base.commit()
        await bot.send_message(message.from_user.id, 'записан в бд')
    else:
        await bot.send_message(message.from_user.id, 'дубль')
# ------------------------------------------------------------------------------------------
# ПОЛУЧЕНИЕ id_users выбранного сотрудника по фамилиии +++++++++++++++++
async def sql_get_id_by_lastname(lastname):#функция изменения бд
    answer = cur.execute(f'SELECT id_users FROM Users WHERE lastname = "{lastname}"')
    return answer.fetchone()[0]

# ------------------------------------------------------------------------------------------
# ДОБАВЛЕНИЕ ОЦЕНКИ и User в NoteUsersRecipient ++++++++++++++++++++++
async def sql_add_note_recipient_command(data):
    cur.execute(f'INSERT INTO NoteUsersRecipient(id_note, id_users ) VALUES ({data["id_note"]}, {data["id_recipient"]})')#?-шифруем значения
    base.commit()

# ------------------------------------------------------------------------------------------
# ДОБАВЛЕНИЕ ОЦЕНКИ и АВТОРА в NoteUsersAuthor ++++++++++++++++++
async def sql_add_note_author_command(data):
    cur.execute(f'INSERT INTO NoteUsersAuthor(id_note, id_users) VALUES ({data["id_note"]}, {data["id_author"]})')#?-шифруем значения
    base.commit()
# ------------------------------------------------------------------------------------------

# мб понадобиться хз что это
async def sql_read(message:types.Message):#получаем событие смс, когда нажимают на кнопку "Меню"
    for ret in cur.execute('SELECT * FROM Users\
                            JOIN UsersDepartment ud ON u.id_users = ud.id_users\
                            WHERE id_department = 10').fetchall():#выгружает в виде списка и получаем в переменную ret
        # markup = InlineKeyboardMarkup()
        # markup.row_width = 2
        # ret = types.InlineKeyboardButton(f'{ret[0]}\nимя: {ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')
        # markup.add(InlineKeyboardButton(ret, callback_data="cb_yes"))
        # # await bot.send_message(message.from_user.id,"Пожалуйста, выберите сотрудника",reply_markup=markup)
        await bot.send_message(message.from_user.id, f'{ret[0]} {ret[-1]}')#0-фото, 1-название и тд
# ------------------------------------------------------------------------------------------
# ЧТЕНИЕ Users ГДЕ id_department = TS ++++++++++++++++++++++++
async def sql_read_users_ts_command():
    return cur.execute('SELECT * FROM Users u\
                            JOIN UsersDepartment ud ON u.id_users = ud.id_users\
                            WHERE id_department = 10 AND deleted = 0').fetchall()#прочитать выборку из таблицы и возвращаем в admin.py delete_item
# ------------------------------------------------------------------------------------------

#  ЧТЕНИЕ Department +++++++++++++++++++++++++
async def sql_read_department():
    return cur.execute('SELECT * FROM Department').fetchall()    



