from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=False, index=True)
    password = Column(String(255), nullable=False)


class Routes(Base):
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=False, unique=True, index=True)
    user_id = Column(Integer, ForeignKey(f'{Users.__tablename__}.id'), index=True)
    duration = Column(String(255))
    points = Column(ARRAY(String(200)), default=list())


class Points(Base):
    __tablename__ = 'points'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=False, unique=True, index=True)
    childs = Column(ARRAY(String(200)), default=list())
    longitude = Column(Float)
    latitude = Column(Float)

