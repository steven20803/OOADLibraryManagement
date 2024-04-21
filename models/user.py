from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class Role(Enum):
    ADMIN = 0
    USER = 1
    GUEST = 2


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(...)
    password: str = Field(...)
    role: Role = Field(default=Role.GUEST)
    status: bool = Field(default=True)
