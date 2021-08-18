import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class Data(Base):
    __tablename__ = 'data'

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    json = Column(Text, nullable=False)
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'text': self.text,
            'json': self.json,
            'id': self.id,
        }


class Records(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True)
    person = Column(Text, nullable=False)
    data_id = Column(Integer, ForeignKey('Data.id'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'person': self.person,
            'data_id': self.data_id,
        }


user = "challenger"
password = "not_the_real_password"
dbname = "coding-challenge-db"
host = "34.84.8.142"


engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:5432/{dbname}')


Base.metadata.create_all(engine)