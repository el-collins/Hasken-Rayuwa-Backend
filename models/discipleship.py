from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel
from typing import Optional

from models.states import States

class DiscipleshipReport(SQLModel, table=True):
    __tablename__ = "discipleship_reports"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    Month: str = Field(index=True)
    State: States = Field(...)
    LGA: str = Field(...)
    Ward: str = Field(...)
    Village: str = Field(...)
    Team: str = Field(...)
    Population: Optional[int] = Field(default=None)
    UPG: Optional[str] = Field(default=None)
    Attendance: Optional[int] = Field(default=None)
    SD_Cards: Optional[int] = Field(default=None)


