from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class MovieModel(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    year = Column(String, index=True, nullable=True)
    rating = Column(Float)
    review = Column(Text)
