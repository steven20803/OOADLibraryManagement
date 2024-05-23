from datetime import datetime
from typing import Optional

from sqlmodel import Column, Field, ForeignKey, Integer, SQLModel
from enum import IntEnum

class BookStatus(IntEnum):
    BORROWED = 0
    AVAILABLE = 1
    LOST = 2
    DAMAGED = 3


class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_name: str = Field(...)
    author: str = Field(...)
    genre: Optional[str] = Field(default=None)
    borrower_id: int = Column(Integer, ForeignKey("user.id"))
    last_borrowed: Optional[datetime] = Field(default=None)
    expected_return_time: Optional[datetime] = Field(default=None)
    added_to_library: datetime = Field(default=datetime.now())
    status: int = Field(default=BookStatus.AVAILABLE)
    comments: str = Field(default="")
