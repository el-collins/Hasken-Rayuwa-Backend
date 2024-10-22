from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field

PyObjectId = Annotated[str, BeforeValidator(str)]


class Link(BaseModel):
    id: PyObjectId = Field(alias="_id")
    url: str = Field(...)
    media_type: str = Field(...)
    title: str | None = Field(...)
    description: str | None = Field(...)