import os
# импортируем модуль emoji для отображения эмоджи
from emoji import emojize

# токен выдается при регистрации приложения
TOKEN = '5884702174:AAHKD6NsPiCzEuqvVHTH8bBzxjW9UgjsRdM'
# название БД
NAME_DB = 'products.db'
# версия приложения
VERSION = '0.0.1'
# автор приложния
AUTHOR = 'User'

# родительская директория
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# путь до базы данных
DATABASE = os.path.join('sqlite:///'+BASE_DIR, NAME_DB)

COUNT = 0

# кнопки управления
KEYBOARD = {
    'CHOOSE_GOODS': emojize(':open_file_folder: Выбрать товар'),
    'INFO': emojize(':speech_balloon: О магазине'),
    'SETTINGS': emojize('⚙️ Настройки'),
    'QUICKSHIT': emojize(':pizza: Полуфабрикаты'),
    'GROCERY': emojize(':bread: Бакалея'),
    'ICE_CREAM': emojize(':shaved_ice: Мороженое'),
    '<<': emojize('⏪'),
    '>>': emojize('⏩'),
    'BACK_STEP': emojize('◀️'),
    'NEXT_STEP': emojize('▶️'),
    'ORDER': emojize('✅ ЗАКАЗ'),
    'X': emojize('❌'),
    'DOWN': emojize('🔽'),
    'AMOUNT_PRODUCT': COUNT,
    'AMOUNT_ORDERS': COUNT,
    'UP': emojize('🔼'),
    'APPLY': '✅ Оформить заказ',
    'COPY': '©️'
}

# id категорий продуктов
CATEGORY = {
    'QUICKSHIT': 1,
    'GROCERY': 2,
    'ICE_CREAM': 3,
}

# названия команд
COMMANDS = {
    'START': "start",
    'HELP': "help",
}
