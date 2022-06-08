from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from geoalchemy2 import Geometry

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=False, index=True)
    dev_type = Column(String(120), nullable=False)


class GeoData(Base):
    __tablename__ = 'geodata'

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    geo_data = Column(Geometry('POINT'))