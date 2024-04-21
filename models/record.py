from sqlmodel import SQLModel, Field, Column, Integer, ForeignKey
from typing import Optional
from datetime import datetime
from .book import Book
from .user import User

class Record(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Column(Integer, ForeignKey('user.id'))
    book_id: int = Column(Integer, ForeignKey('book.id'))
    borrowed_time: datetime = Field(...)
    expected_return_time: datetime = Field(...)
    actual_return_time: Optional[datetime] = Field(default=None)