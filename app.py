from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# SQLAlchemy configuration
DATABASE_URL = "mysql://root:GcBi54404@localhost/book_management"  # Database connection string.

# Create SQLAlchemy engine and sessionmaker
engine = create_engine(DATABASE_URL, connect_args={"charset": "utf8mb4"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# SQLAlchemy model for a Book
class Book(Base):
    """
    SQLAlchemy model representing the 'books' table in the database.
    """
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    isbn = Column(String(13), unique=True, nullable=False)  # ISBN must be unique.
    published_year = Column(Integer, nullable=False)

# FastAPI instance
app = FastAPI()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for validation
class BookCreate(BaseModel):
    """
    Pydantic schema for validating input data when creating or updating books.
    """
    title: str
    author: str
    description: str = None
    isbn: str
    published_year: int

class BookOut(BookCreate):
    """
    Pydantic schema for output data when returning book information.
    Includes the book ID.
    """
    id: int

    class Config:
        orm_mode = True

# Initialize the database (create tables if they don't exist)
Base.metadata.create_all(bind=engine)

# Routes
@app.get("/books", response_model=List[BookOut])
def get_books(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all books.
    """
    books = db.query(Book).all()
    return books

@app.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve a specific book by ID.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books", response_model=BookOut)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Endpoint to create a new book.
    """
    db_book = Book(
        title=book.title,
        author=book.author,
        description=book.description,
        isbn=book.isbn,
        published_year=book.published_year,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.put("/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, updated_book: BookCreate, db: Session = Depends(get_db)):
    """
    Endpoint to update an existing book.
    """
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db_book.title = updated_book.title
    db_book.author = updated_book.author
    db_book.description = updated_book.description
    db_book.isbn = updated_book.isbn
    db_book.published_year = updated_book.published_year
    
    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to delete a book by ID.
    """
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_book)
    db.commit()
    return {"message": f"Book with ID {book_id} deleted"}
