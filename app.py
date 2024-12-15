from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Book
from pydantic import BookCreate, Book
from mysqldb import SessionLocal, engine, Base

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/books/", response_model=Book)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(
        title=book.title,
        author=book.author,
        published_date=book.published_date,
        isbn=book.isbn,
        pages=book.pages,
        language=book.language
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/books/", response_model=list[Book])
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db_book.title = book.title
    db_book.author = book.author
    db_book.published_date = book.published_date
    db_book.isbn = book.isbn
    db_book.pages = book.pages
    db_book.language = book.language

    db.commit()
    db.refresh(db_book)
    return db_book

@app.delete("/books/{book_id}", response_model=Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_book)
    db.commit()
    return db_book
