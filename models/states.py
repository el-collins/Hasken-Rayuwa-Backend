from pydantic import BaseModel, BeforeValidator, Field
from enum import Enum
from typing import Annotated


# Custom type for MongoDB ObjectId
# PyObjectId = Annotated[str, Field(default_factory=lambda: str(ObjectId()))]



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
    

PyObjectId = Annotated[str, BeforeValidator(str)]


    
class StateData(BaseModel):
    # id: Optional[PyObjectId] = Field(alias="_id", default=None)    
    id: PyObjectId = Field(alias="_id")
    State: States
    Lga: str 
    Ward: str 
    Village: str 
    Estimated_Christian_Population: int 
    Estimated_Muslim_Population: int 
    Estimated_Traditional_Religion_Population: int 
    Converts: int = Field(ge=0)
    Estimated_Total_Population: int = 0
    Film_Attendance: int 
    People_Group: str 
    Practiced_Religion: str 


