from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove

b1 = KeyboardButton('/Оставить_оценку')
# b2 = KeyboardButton('/Расположение')
# b3 = KeyboardButton('/Меню')
# b4 = KeyboardButton('Поделиться номером', request_contact=True)
# b5 = KeyboardButton('Отправить где я', request_location=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)#, one_time_keyboard=True) #заменяем команды на кнопки, скрытие клавы после нажатия ком

kb_client.add(b1)#.add(b3)#.add(b3)#.row(b4, b5)
# kb_client.row(b1,b2,b3) #в одну строку кнопки
# kb_client.add(b1).add(b2).insert(b3) #add-всю строку занимает кнопка, insert-добавляет в предыдущую по свободному месту