from sqlalchemy import Column, Integer, String, Date
from mysqldb import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    published_date = Column(Date)
    isbn = Column(String, unique=True)
    pages = Column(Integer)
    language = Column(String)
