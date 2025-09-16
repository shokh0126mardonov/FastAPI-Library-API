from pydantic import BaseModel
from typing import Optional
from models import Genre


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
        orm_mode = True   # SQLAlchemy obyektlarini avtomatik JSON ga aylantiradi
