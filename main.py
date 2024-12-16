from fastapi import Depends, FastAPI, HTTPException  # Importing FastAPI classes and functions for API development.
from pydantic import BaseModel  # Importing BaseModel for data validation and serialization.
from typing import List  # Importing List for type hinting of list responses.
from sqlalchemy import create_engine, Column, Integer, String  # Importing SQLAlchemy components for ORM mapping.
from sqlalchemy.ext.declarative import declarative_base  # Base class for SQLAlchemy models.
from sqlalchemy.orm import sessionmaker, Session  # Tools for session management in SQLAlchemy.

# SQLAlchemy configuration
DATABASE_URL = "mysql://root:GcBi54404@localhost/book_management"  # Database connection string for MySQL.

# Create SQLAlchemy engine and sessionmaker
engine = create_engine(DATABASE_URL, connect_args={"charset": "utf8mb4"})  # Engine for interacting with the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Session factory for database interactions.

# Base class for models
Base = declarative_base()  # Base class for all ORM models.

# SQLAlchemy model for a Book
class Book(Base):
    """
    SQLAlchemy model representing the 'books' table in the database.
    """
    __tablename__ = "books"  # Specifies the table name in the database.
    id = Column(Integer, primary_key=True, index=True)  # ID column as the primary key.
    title = Column(String(255), nullable=False)  # Title column with a max length of 255, cannot be null.
    author = Column(String(255), nullable=False)  # Author column with a max length of 255, cannot be null.
    description = Column(String(500), nullable=True)  # Optional description column with a max length of 500.
    isbn = Column(String(13), unique=True, nullable=False)  # ISBN column must be unique and cannot be null.
    published_year = Column(Integer, nullable=False)  # Year of publication, cannot be null.

# FastAPI instance
app = FastAPI()  # Initializing the FastAPI application.

# Dependency to get the DB session
def get_db():
    """
    Provides a database session for each request.
    """
    db = SessionLocal()  # Create a new database session.
    try:
        yield db  # Yield the session to the request handler.
    finally:
        db.close()  # Close the session after the request.

# Pydantic models for validation
class BookCreate(BaseModel):
    """
    Pydantic schema for validating input data when creating or updating books.
    """
    title: str  # Book title as a required string.
    author: str  # Author name as a required string.
    description: str = None  # Optional description of the book.
    isbn: str  # ISBN as a required string.
    published_year: int  # Year of publication as a required integer.

class BookOut(BookCreate):
    """
    Pydantic schema for output data when returning book information.
    Includes the book ID.
    """
    id: int  # Book ID as an integer.

    class Config:
        orm_mode = True  # Enables compatibility with ORM objects.

# Initialize the database (create tables if they don't exist)
Base.metadata.create_all(bind=engine)  # Automatically creates tables based on the models.

# Routes
@app.get("/books", response_model=List[BookOut])  # Route to get all books.
def get_books(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all books.
    """
    books = db.query(Book).all()  # Query all books from the database.
    return books  # Return the list of books.

@app.get("/books/{book_id}", response_model=BookOut)  # Route to get a book by ID.
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve a specific book by ID.
    """
    book = db.query(Book).filter(Book.id == book_id).first()  # Query the book with the given ID.
    if not book:  # If the book doesn't exist, raise a 404 error.
        raise HTTPException(status_code=404, detail="Book not found")
    return book  # Return the book.

@app.post("/books", response_model=BookOut)  # Route to create a new book.
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
    )  # Create a new Book instance.
    db.add(db_book)  # Add the book to the session.
    db.commit()  # Commit the transaction to save the book.
    db.refresh(db_book)  # Refresh the instance with the latest data.
    return db_book  # Return the created book.

@app.put("/books/{book_id}", response_model=BookOut)  # Route to update a book.
def update_book(book_id: int, updated_book: BookCreate, db: Session = Depends(get_db)):
    """
    Endpoint to update an existing book.
    """
    db_book = db.query(Book).filter(Book.id == book_id).first()  # Query the book with the given ID.
    if not db_book:  # If the book doesn't exist, raise a 404 error.
        raise HTTPException(status_code=404, detail="Book not found")
    
    db_book.title = updated_book.title  # Update the title.
    db_book.author = updated_book.author  # Update the author.
    db_book.description = updated_book.description  # Update the description.
    db_book.isbn = updated_book.isbn  # Update the ISBN.
    db_book.published_year = updated_book.published_year  # Update the publication year.
    
    db.commit()  # Commit the transaction to save changes.
    db.refresh(db_book)  # Refresh the instance with the latest data.
    return db_book  # Return the updated book.

@app.delete("/books/{book_id}")  # Route to delete a book by ID.
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to delete a book by ID.
    """
    db_book = db.query(Book).filter(Book.id == book_id).first()  # Query the book with the given ID.
    if not db_book:  # If the book doesn't exist, raise a 404 error.
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_book)  # Delete the book from the session.
    db.commit()  # Commit the transaction to finalize deletion.
    return {"message": f"Book with ID {book_id} deleted"}  # Return a success message.
