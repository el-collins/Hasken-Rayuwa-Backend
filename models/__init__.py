from sqlmodel import SQLModel

from .states import StateData #noqa
from .links import Link #noqa
from .users import User, ContactUser, VolunteerUser #noqa

metadata = SQLModel.metadata