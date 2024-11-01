from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


engine = create_engine('sqlite:///taskmanager.db', echo=True)

SessionLocal = sessionmaker(bind=engine)    # создаем локальную сессию для связи с нашей БД


class Base(DeclarativeBase):    # базовый класс Base для других моделей, наследуется от 'DeclarativeBase'
    pass
