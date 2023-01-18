from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *

Base = declarative_base()


class Links(Base):
    __tablename__ = 'links'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    link = Column(String(255), nullable=False, unique=True, index=True)
    click_cost = Column(Integer, nullable=False, index=True)
    date = Column(DateTime, server_default=func.now(), nullable=False)


class Views(Base):
    __tablename__ = 'views'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    link_id = Column(Integer, ForeignKey(f'{Links.__tablename__}.id'), nullable=False,)
    date = Column(DateTime, server_default=func.now(), nullable=False)


class Clicks(Base):
    __tablename__ = 'clicks'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    link_id = Column(Integer, ForeignKey(f'{Links.__tablename__}.id'), nullable=False)
    date = Column(DateTime, server_default=func.now(), nullable=False)


