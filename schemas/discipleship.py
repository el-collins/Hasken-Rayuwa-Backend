from pydantic import BaseModel
from typing import Optional


from models.states import States

class DiscipleshipReportCreate(BaseModel):
    Month: str
    State: States 
    LGA: str
    Ward: str
    Village: str
    Team: str
    Population: Optional[int] = None
    UPG: Optional[str] = None
    Attendance: Optional[int] = None
    SD_Cards: Optional[int] = None
    Manuals_Given: Optional[int] = None
    Bibles_Given: Optional[int] = None
   


class DiscipleshipReportUpdate(BaseModel):
    Month: Optional[str] = None
    State: Optional[str] = None
    LGA: Optional[str] = None
    Ward: Optional[str] = None
    Village: Optional[str] = None
    Team: Optional[str] = None
    Population: Optional[int] = None
    UPG: Optional[str] = None
    Attendance: Optional[int] = None
    SD_Cards: Optional[int] = None
    Manuals_Given: Optional[int] = None
    Bibles_Given: Optional[int] = None
    
