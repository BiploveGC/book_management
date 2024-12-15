from pydantic import BaseModel
from datetime import date

class BookBase(BaseModel):
    title: str
    author: str
    published_date: date
    isbn: str
    pages: int
    language: str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        orm_mode = True
