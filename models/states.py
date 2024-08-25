from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel
from enum import Enum

class States(str, Enum):
    """
    Enum representing states in Nigeria.
    """
    Abia = "Abia"
    Adamawa = "Adamawa"
    AkwaIbom = "Akwa Ibom"
    Anambra = "Anambra"
    Bauchi = "Bauchi"
    Bayelsa = "Bayelsa"
    Benue = "Benue"
    Borno = "Borno"
    Cross_River = "Cross River"
    Delta = "Delta"
    Ebonyi = "Ebonyi"
    Edo = "Edo"
    Ekiti = "Ekiti"
    Enugu = "Enugu"
    FCT = "FCT"
    Gombe = "Gombe"
    Imo = "Imo"
    Jigawa = "Jigawa"
    Kaduna = "Kaduna"
    Kano = "Kano"
    Katsina = "Katsina"
    Kebbi = "Kebbi"
    Kogi = "Kogi"
    Kwara = "Kwara"
    Lagos = "Lagos"
    Nasarawa = "Nasarawa"
    Niger = "Niger"
    Ogun = "Ogun"
    Ondo = "Ondo"
    Osun = "Osun"
    Oyo = "Oyo"
    Plateau = "Plateau"
    Rivers = "Rivers"
    Sokoto = "Sokoto"
    Taraba = "Taraba"
    Yobe = "Yobe"
    Zamfara = "Zamfara"
    
    
class ReligionType(str, Enum):
    """
    Represents types of religions.
    """
    Christianity = "Christianity"
    Islam = "Islam"
    Traditional = "Traditional"
    Other = "Other"
    
    
class StateData(SQLModel, table=True):
    __tablename__ = "state_data"
    
    id: UUID = Field(
        default_factory=uuid4, 
        primary_key=True)
    
    State: States = Field(...)
    Lga: str = Field(index=True)
    Ward: str = Field(...)
    Village: str = Field(...)
    Estimated_Christian_Population: int = Field(...)
    Estimated_Muslim_Population: int = Field(...)
    Estimated_Traditional_Religion_Population: int = Field(...)
    Converts: int = Field(ge=0)
    Estimated_Total_Population: int = Field(default=0)
    Film_Attendance: int = Field(...)
    People_Group: str = Field(...)
    Practiced_Religion: str = Field(...)
