from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List

from database import Base, engine, get_db
from models import Book, Genre

# DB jadval yaratish
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NT-Kutubxona-library")

# --- Pydantic Schemas ---
class BookBase(BaseModel):
    title: str
    author: str
    pages: int
    description: Optional[str] = None
    genre: Genre

class BookCreate(BookBase):
    pass

class BookRead(BookBase):
    book_id: int

    class Config:
        orm_mode = True


# --- ROUTES ---
@app.get("/api/books/", response_model=List[BookRead])
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@app.post("/api/books/", response_model=BookRead)
def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    new_book = Book(
        title=book_data.title,
        author=book_data.author,
        pages=book_data.pages,
        description=book_data.description,
        genre=book_data.genre
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.get("/api/books/{book_id}", response_model=BookRead)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.book_id == book_id).first()
    if not book:
        return {"error": "Book not found"}
    return book
