# импортируем библиотеку abc для реализации абстрактных классов
import abc
# импортируем разметку клавиатуры и клавиш
from markup.markup import Keyboards
# импортируем класс-менеджер для работы с библиотекой
from data_base.dbalchemy import DBManager


# как я понял, абс библиотека позволяет делать классы-шаблоны, потому и называется abstract base class
# и соответственно все что тут описано, должно быть определено/переопределено в наследниках

class Handler(metaclass=abc.ABCMeta):

    def __init__(self, bot):
        # получаем объект бота
        self.bot = bot
        # инициализируем разметку кнопок
        self.keybords = Keyboards()
        # инициализируем менеджер для работы с БД
        self.BD = DBManager()

    # заглушка
    @abc.abstractmethod
    def handle(self):
        pass
