from os import path
from datetime import datetime

# ф-ция для создания объекта подключения к бд
from sqlalchemy import create_engine
# все операции с базой выполняются через сессию, создает сессию
from sqlalchemy.orm import sessionmaker
# базовый класс, необходим для переноса всех изменений в моделях на структуру таблиц в бд
from data_base.dbcore import Base
from settings import utility

# конфиг с константами для бд
from settings import config
# собственно модель продуктов
from models.product import Products
from models.order import Order

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

    def close(self):
        """
        Закрывает сесию
        """
        self._session.close()

    # принимает категорию и возвращает все товары относящиеся к ней
    def select_all_products_category(self, category):
        """
        Возвращает все товары категории
        """
        result = self._session.query(Products).filter_by(
            category_id=category).all()

        self.close()
        return result

    # Работа с заказом
    def _add_orders(self, quantity, product_id, user_id,):
        """
        Метод заполнения заказа
        """
        # получаем список всех product_id
        all_id_product = self.select_all_product_id()
        # если данные есть в списке, обновляем таблицы заказа и продуктов
        if product_id in all_id_product:
            quantity_order = self.select_order_quantity(product_id)
            quantity_order += 1
            self.update_order_value(product_id, 'quantity', quantity_order)

            quantity_product = self.select_single_product_quantity(product_id)
            quantity_product -= 1
            self.update_product_value(product_id, 'quantity', quantity_product)
            return
        # если данных нет, создаем новый объект заказа
        else:
            order = Order(quantity=quantity, product_id=product_id,
                          user_id=user_id, data=datetime.now())
            quantity_product = self.select_single_product_quantity(product_id)
            quantity_product -= 1
            self.update_product_value(product_id, 'quantity', quantity_product)

        self._session.add(order)
        self._session.commit()
        self.close()

    # конвертирует список с p[(5,),(8,),...] к [5,8,...]
    def select_all_product_id(self):
        """
        Возвращает все id товара в заказе
        """
        result = self._session.query(Order.product_id).all()
        self.close()
        # конвертируем результат выборки в вид [1,3,5...]
        return utility._convert(result)

    def select_order_quantity(self, product_id):
        """
        Возвращает количество товара в заказе
        """
        result = self._session.query(Order.quantity).filter_by(
            product_id=product_id).one()
        self.close()
        return result.quantity

    def select_single_product_quantity(self, rownum):
        """
        Возвращает количество товара на складе
        в соответствии с номером товара - rownum
        Этот номер определяется при выборе товара в интерфейсе.
        """
        result = self._session.query(
            Products.quantity).filter_by(id=rownum).one()
        self.close()
        return result.quantity

    def update_product_value(self, rownum, name, value):
        """
        Обновляет количество товара на складе
        в соответствии с номером товара - rownum
        """
        self._session.query(Products).filter_by(
            id=rownum).update({name: value})
        self._session.commit()
        self.close()

    def update_order_value(self, product_id, name, value):
        """
        Обновляет данные указанной позиции заказа
        в соответствии с номером товара - rownum
        """
        self._session.query(Order).filter_by(
            product_id=product_id).update({name: value})
        self._session.commit()
        self.close()

    def select_single_product_name(self, rownum):
        """
        Возвращает название товара
        в соответствии с номером товара - rownum
        """
        result = self._session.query(Products.name).filter_by(id=rownum).one()
        self.close()
        return result.name

    def select_single_product_title(self, rownum):
        """
        Возвращает торговую марку товара
        в соответствии с номером товара - rownum
        """
        result = self._session.query(Products.title).filter_by(id=rownum).one()
        self.close()
        return result.title

    def select_single_product_price(self, rownum):
        """
        Возвращает цену товара
        в соответствии с номером товара - rownum
        """
        result = self._session.query(Products.price).filter_by(id=rownum).one()
        self.close()
        return result.price

    def count_rows_order(self):
        """
        Возвращает количество позиций в заказе
        """
        result = self._session.query(Order).count()
        self.close()
        return result

    def select_order_quantity(self, product_id):
        """
        Возвращает количество товара из заказа
        в соответствии с номером товара - rownum
        """
        result = self._session.query(Order.quantity).filter_by(
            product_id=product_id).one()
        self.close()
        return result.quantity
