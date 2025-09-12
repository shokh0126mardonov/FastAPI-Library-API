from typing import Annotated
from enum import Enum
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field
from database import Base, engine, Session
from models import Book


app = FastAPI(title="NT-Kutubxona API")

Base.metadata.create_all(engine)


@app.get("/api/books/{book_id}")
def get_book_detail(
    # book_id: int = Path(title="bitta kitob id si", ge=1, le=1000),
    book_id: Annotated[int, Path(title="bitta kitob id si", ge=1, le=1000)]
):
    return {"book": book_id}


@app.get("/api/users/{username}")
def get_user_detail(
    # username: str = Path(min_length=5, max_length=30, pattern='^[a-z0-9_-]{5,30}$')
    username: Annotated[str, Path(min_length=5, max_length=30, pattern='^[a-z0-9_-]{5,30}$')]
):
    return {"username": username}


@app.get("/api/books/")
def get_book_list(
    # author: str = Query(title="kitob muallifi", min_length=5, max_length=30)
    author: Annotated[str, Query(title="kitob muallifi", min_length=5, max_length=30)]
):
    return {"author": author}


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
    book_data: BookCreate
):
    db = Session()

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
