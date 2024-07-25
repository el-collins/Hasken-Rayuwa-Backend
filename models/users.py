from uuid import UUID, uuid4
from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlmodel import Field, SQLModel, Column, Text

class User(SQLModel, table=True):
    __tablename__ = 'users'
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    fullname: str = Field(...)
    email: EmailStr | None = Field(sa_column=Column("email", Text, nullable=False, unique=True))

class ContactUser(SQLModel, table=True):
    __tablename__ = 'contact'
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    fullname: str = Field(...)
    email: EmailStr = Field(sa_column=Column("contact_email", Text, nullable=False))
    message: str = Field(default="message")

class VolunteerUser(SQLModel, table=True):
    __tablename__ = 'volunteer'
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    fullname: str = Field(...)
    email: EmailStr = Field(sa_column=Column("volunteer_email", Text, nullable=False))
    phone_number: PhoneNumber | None = Field(default="phone_number")
    address: str = Field(default="address")
