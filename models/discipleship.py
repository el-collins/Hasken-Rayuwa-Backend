from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import date

from models.states import States


class DiscipleshipReport(SQLModel, table=True):
    __tablename__ = "discipleship_reports"  # type: ignore

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    Year: int = Field(default=date.today().year)
    CreatedAt: date = Field(default=date.today())
    Month: str = Field(index=True)
    State: States = Field(index=True)
    LGA: str = Field(...)
    Ward: str = Field(...)
    Village: str = Field(...)
    Team: str = Field(...)
    Population: Optional[int] = Field(default=None)
    UPG: Optional[str] = Field(default=None)
    Attendance: Optional[int] = Field(default=None)
    SD_Cards: Optional[int] = Field(default=None)
    Manuals_Given: Optional[int] = Field(default=None)
    Bibles_Given: Optional[int] = Field(default=None)
