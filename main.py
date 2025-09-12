from typing import Annotated
from enum import Enum
from fastapi import FastAPI, Path, Query, Depends
from pydantic import BaseModel, Field
from database import Base, engine, Session, get_db
from models import Book


app = FastAPI(title="NT-Kutubxona API")

Base.metadata.create_all(engine)


@app.get("/api/books/{book_id}")
def get_book_detail(
    # book_id: int = Path(title="bitta kitob id si", ge=1, le=1000),
    book_id: Annotated[int, Path(title="bitta kitob id si", ge=1, le=1000)],
    db: Annotated[Session, Depends(get_db)]
):

    result = db.query(Book).filter(Book.book_id==book_id).first()
    if result:
        return {
            "id": result.book_id,
            "title": result.title,
            "desciption": result.description,
            "author": result.author,
            "genre": result.genre,
            "pages": result.pages,
        }
    return {"message": "bunday kitob mavjud emas"}


@app.get("/api/users/{username}")
def get_user_detail(
    # username: str = Path(min_length=5, max_length=30, pattern='^[a-z0-9_-]{5,30}$')
    username: Annotated[str, Path(min_length=5, max_length=30, pattern='^[a-z0-9_-]{5,30}$')],
    db: Annotated[Session, Depends(get_db)]
):
    return {"username": username}


@app.get("/api/books/")
def get_book_list(
    # author: str = Query(title="kitob muallifi", min_length=5, max_length=30)
    db: Annotated[Session, Depends(get_db)],
    author: Annotated[str | None, Query(title="kitob muallifi", min_length=5, max_length=30)] = None,
):
    result = []
    books = db.query(Book).all()
    for book in books:
        result.append({
            "id": book.book_id,
            "title": book.title,
            "desciption": book.description,
            "author": book.author,
            "genre": book.genre,
            "pages": book.pages,
        })
    return result


class Genre(str, Enum):
    roman = "roman"
    story = "hikoya"
    drama = "drama"


class BookCreate(BaseModel):
    # title: str = Field(min_length=5, max_length=30)
    title: Annotated[str, Field(title="kitob nomi", min_length=5, max_length=30)]
    # author: str = Field(title="kitob muallifi", min_length=5, max_length=30)
    author: Annotated[str, Field(title="kitob muallifi", min_length=5, max_length=30)]
    # pages: int = Field(title="varoqlar soni", ge=1, le=1000)
    pages: Annotated[int, Field(title="varoqlar soni", ge=1, le=1000)]
    # description: str | None = Field(default=None, title="tarifi")
    description: Annotated[str | None, Field(default=None, title="tarifi")] = None
    genre: Genre


@app.post("/api/books/")
def create_book(
    book_data: BookCreate,
    db: Annotated[Session, Depends(get_db)]
):

    book = Book(
        title=book_data.title,
        author=book_data.author,
        pages=book_data.pages,
        description=book_data.description,
        genre=book_data.genre
    )

    db.add(book)

    db.commit()
    
    return {}
