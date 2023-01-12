from os import path

# ф-ция для создания объекта подключения к бд
from sqlalchemy import create_engine
# все операции с базой выполняются через сессию, создает сессию
from sqlalchemy.orm import sessionmaker
# базовый класс, необходим для переноса всех изменений в моделях на структуру таблиц в бд
from data_base.dbcore import Base

# конфиг с константами для бд
from settings import config
# собственно модель продуктов
from models.product import Products

class Singleton(type):
    """
    Патерн Singleton предоставляет механизм создания одного
    и только одного объекта класса,
    и предоставление к нему глобальную точку доступа.
    """
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class DBManager(metaclass=Singleton):
    """ 
    Класс-менеджер для работы с БД
    """

    def __init__(self):
        """
        Инициализация сесии и подключения к БД
        """
        # подключение к бд. config.DATABASE - путь до бд
        self.engine = create_engine(config.DATABASE)
        # создаем класс сессии
        session = sessionmaker(bind=self.engine)
        # создаем объект сессии
        self._session = session()
        # если структуры базы данных нету
        if not path.isfile(config.DATABASE):
            # создаем все как в джанго с makemigrations-migrate
            # эта база должна объединять все модели сразу как с dbcore.py
            # иначе все скорее всего в сломанном порядке создатся
            Base.metadata.create_all(self.engine)

    # принимает категорию и возвращает все товары относящиеся к ней
    def select_all_products_category(self, category):
        """
        Возвращает все товары категории
        """
        # аналог джанговского products.ojects.filter(category=whatever)
        result = self._session.query(Products).filter_by(
            category_id=category).all()

        self.close()
        return result

    def close(self):
        """ Закрывает сессию """
        self._session.close()