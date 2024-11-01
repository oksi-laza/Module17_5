from app.backend.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import CreateTable    # для вывода SQL-запроса в консоли
from app.models import *


class Task(Base):
    __tablename__ = 'tasks'
    __table_args__ = {'extend_existing': True}    # указали SQLAlchemy расширить существующее определение таблицы, а не создавать новое
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer, default=0)     # По умолчанию 0 - это default?
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)    # внешний ключ на id из таблицы 'users', не NULL
    slug = Column(String, unique=True, index=True)

    user = relationship('User', back_populates='tasks')


# Вывести SQL-запрос в консоли
print(CreateTable(Task.__table__))
