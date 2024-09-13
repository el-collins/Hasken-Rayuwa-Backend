# from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel
from datetime import datetime, timezone

class Blog(SQLModel, table=True):
    __tablename__ = 'blogs' # type: ignore
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(...)
    author: str = Field(...)
    content: str = Field(...)
    # visibility: str = Field(default="active")  # Options: "active" or "inactive"
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# class BlogCreate(SQLModel):
#     title: str
#     author: str
#     content: str
#     visibility: Optional[str] = Field(default="active") 