from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

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