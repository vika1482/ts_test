#промежуточный файл, тут создаются экземпляры бота
from aiogram import Bot #импортируем класс Бота и типы функций
from aiogram.dispatcher import Dispatcher #улавливает сообщения
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage #этот класс позволяет хранить данные в ОП (PS есть другие хранилища-2)

storage = MemoryStorage()

bot = Bot(token=os.getenv('TOKEN'))#инициализируем бота
dp = Dispatcher(bot, storage=storage)#storage-место где будут храниться данные user