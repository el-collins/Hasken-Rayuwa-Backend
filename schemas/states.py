# schemas.py
from pydantic import BaseModel, validator
from typing import List, Union
from fastapi import UploadFile
from models.states import States, ReligionType


class StateDataInput(BaseModel):
    state: States
    lga: str
    ward: str
    village: str
    estimated_christian_population: int
    estimated_muslim_population: int
    estimated_traditional_religion_population: int
    converts: int
    estimated_total_population: int = 0
    film_attendance: int
    people_group: str
    practiced_religion: ReligionType