from datetime import datetime
from typing import Optional

from sqlmodel import Column, Field, ForeignKey, Integer, SQLModel, String
from typing import List, Optional

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_name: str = Field(default=None, unique=True)
    author: str = Field(default=None)
    borrowed: bool = Field(default=False)
    borrower_id: int = Field(default=None, foreign_key="user.id")
    last_borrowed: Optional[datetime] = Field(default=None)
    status: bool = Field(default=True)
    comments: str = Field(default="") 
