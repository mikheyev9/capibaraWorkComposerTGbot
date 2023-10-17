from sqlalchemy import TEXT, BigInteger, Boolean, Column, Integer
from sqlalchemy.dialects import sqlite
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker
from .config import DATABASE_URL

BigIntegerType = BigInteger()
BigIntegerType = BigIntegerType.with_variant(sqlite.INTEGER(), 'sqlite')


class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)


class Users(Base):
    id_in_work_composer = Column(TEXT, unique=True)
    fio = Column(TEXT)


class Projects(Base):
    id_in_work_composer = Column(TEXT, unique=True)
    title = Column(TEXT)


class Tasks(Base):
    id_in_work_composer = Column(TEXT, unique=True)
    id_projects = Column(TEXT)
    id_users = Column(TEXT)
    title = Column(TEXT)
    description = Column(TEXT)
    author = Column(TEXT)
    status = Column(TEXT)
    id_project_site = Column(TEXT, default='')


class ChatId(Base):
    chat_id = Column(TEXT, unique=True)


class ProjectsSite(Base):
    is_complite = Column(Boolean, default=False)
    row = Column(TEXT)
    project = Column(TEXT)
    create_project = Column(TEXT)
    parsing = Column(TEXT)
    verstka = Column(TEXT)
    buy_domain = Column(TEXT)
    deploy = Column(TEXT)
    content = Column(TEXT)
    acquiring = Column(TEXT)
    release = Column(TEXT)


print(DATABASE_URL)
engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)
