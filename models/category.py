# компоненты библиотеки для описания структуры таблицы
from sqlalchemy import Column, String, Integer, Boolean
# класс-конструктор для работы с декларативным стилем работы с SQLAlchemy
# from sqlalchemy.ext.declarative import declarative_base
# инициализация декларативного стиля
# это выдаст ошибку
# Base = declarative_base()

from data_base.dbcore import Base


class Category(Base):
    """
    Класс-модель для описания таблицы "Категория товара",
    основан на декларативном стиле SQLAlchemy
    """
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    is_active = Column(Boolean)

    def __str__(self):
        """
        Метод возвращает строковое представление объекта класса
        """
        return self.name
