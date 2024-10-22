from typing import Annotated, Optional
from datetime import date

from pydantic import BaseModel, BeforeValidator, Field

from models.states import States

PyObjectId = Annotated[str, BeforeValidator(str)]


class DiscipleshipReport(BaseModel):
    id: PyObjectId = Field(alias="_id")
    Year: int = Field(default_factory=lambda: date.today().year)
    CreatedAt: date = Field(default_factory=date.today)
    Month: str
    State: States
    LGA: Optional[str] = None
    Ward: str
    Village: str
    Team: str
    Population: Optional[int] = None
    UPG: Optional[str] = None
    Attendance: Optional[int] = None
    SD_Cards: Optional[int] = None
    Manuals_Given: Optional[int] = None
    Bibles_Given: Optional[int] = None
