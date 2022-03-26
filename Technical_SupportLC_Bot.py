#в этом файле происходит запуск бота
from aiogram.utils import executor #для запуска бота, чтобы он вышел в онлайн
from create_bot import dp 
from data_base import sqlite_db


async def on_startup(_):
    print('Бот вышел в онлайн')#еще тут подлкючение к БД будет
    sqlite_db.sql_start()

from handlers import client, admin, other

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
# other.register_handlers_other(dp)


executor.start_polling(dp,skip_updates=True, on_startup=on_startup) #без этой команты, пока бот не онл все смс сохранятся и ему придется на них отвечать
