from datetime import date
from typing import Annotated, Optional

from pydantic import BaseModel, BeforeValidator, Field
from models.states import States


PyObjectId = Annotated[str, BeforeValidator(str)]


class FilmShowReport(BaseModel):
    id: PyObjectId = Field(alias="_id")
    Year: int = Field(default_factory=lambda: date.today().year)
    CreatedAt: date = Field(default_factory=date.today)
    Team: str 
    State: States 
    Ward: str 
    Village: str 
    LGA: Optional[str] = None
    Population: Optional[int] = None
    UPG: Optional[str] = None
    Attendance: int = Field(...)
    SD_Cards: Optional[int] = None
    Audio_Bibles: Optional[int] = None
    People_Saved: Optional[int] = None
    Date: Optional[str] = Field(...)
    Month: str 
