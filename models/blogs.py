# from typing import Optional
from typing import Annotated
from datetime import datetime, timezone

from pydantic import BaseModel, BeforeValidator, Field

PyObjectId = Annotated[str, BeforeValidator(str)]

class Blog(BaseModel):
    id: PyObjectId = Field(alias="_id")
    title: str 
    author: str 
    content: str 
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


