from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel
from datetime import date
from typing import Optional
from models.states import States

class FilmShowReport(SQLModel, table=True):
    __tablename__: str = "film_show_reports"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    Team: str = Field(...)
    State: States = Field(...)
    Ward: str = Field(...)
    Village: str = Field(...)
    LGA: Optional[str] = Field(default=None)
    Population: Optional[int] = Field(default=None)
    UPG: Optional[str] = Field(default=None)
    Attendance: int = Field(...)
    SD_Cards: Optional[int] = Field(default=None)
    Audio_Bibles: Optional[int] = Field(default=None)
    People_Saved: Optional[int] = Field(default=None)
    Date: date = Field(...)
    Month: str = Field(...)

