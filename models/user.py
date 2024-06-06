from enum import IntEnum
from typing import Optional

from sqlmodel import Field, SQLModel
from sqlmodel import Session, select
from typing import List


class Role(IntEnum):
    ADMIN = 0
    USER = 1
    GUEST = 2


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...)
    password: str = Field(...)
    role: int = Field(default=Role.GUEST)
    birthdate: Optional[str] = Field(default=None)
    status: bool = Field(default=True)
