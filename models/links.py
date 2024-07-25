from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel

class Link(SQLModel, table=True):
    __tablename__ = 'links'
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    url: str = Field(unique=True, index=True)
    media_type: str = Field(index=True)
    title: str | None = Field(...)
    description: str | None = Field(...)