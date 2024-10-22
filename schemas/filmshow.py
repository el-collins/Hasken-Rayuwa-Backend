from pydantic import BaseModel, Field
from typing import Optional



from models.states import States


class FilmShowReportCreate(BaseModel):
    Month: str
    State: States = Field(...)
    LGA: str
    Ward: str
    Village: str
    Team: str
    Population: Optional[int] = None
    UPG: Optional[str] = None
    Attendance: Optional[int] = None
    SD_Cards: Optional[int] = None
    Audio_Bibles: Optional[int] = None
    People_Saved: Optional[int] = None
    Date: Optional[str] = None


class FilmShowReportUpdate(BaseModel):
    Team: Optional[str] = None
    State: Optional[str] = None
    LGA: Optional[str] = None
    Ward: Optional[str] = None
    Village: Optional[str] = None
    Population: Optional[int] = None
    UPG: Optional[str] = None
    Attendance: Optional[int] = None
    SD_Cards: Optional[int] = None
    Audio_Bibles: Optional[int] = None
    People_Saved: Optional[int] = None
    Date: Optional[str] = None
    Month: Optional[str] = None
