from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, Text, DateTime, CheckConstraint, Enum as SqlEnum
from database import Base
from datetime import datetime

class Genre(str, PyEnum):
    roman = "roman"
    story = "hikoya"
    drama = "drama"

class Book(Base):
    __tablename__ = "books"

    book_id = Column("id", Integer, primary_key=True, index=True, nullable=False)
    title = Column(String(length=30), nullable=False)
    author = Column(String(length=30), nullable=False)
    description = Column(Text)
    pages = Column(Integer, CheckConstraint("pages >= 1"), nullable=False)
    genre = Column(SqlEnum(Genre), nullable=False)

    created_at = Column("created_at", DateTime, default=datetime.now)
    updated_at = Column("updated_at", DateTime, onupdate=datetime.now)
