from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///books.db')
Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, default="TITLE")
    price = Column(Float,default="PRICE")
    availability = Column(Boolean,default="AVAILABILITY")
    rating = Column(Integer,default="RATING")

Base.metadata.create_all(engine)


