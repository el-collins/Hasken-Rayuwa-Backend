"""Initial migration on the new sqlite database

Revision ID: f39d872f189b
Revises: 6465ad9e9f58
Create Date: 2024-09-13 15:50:51.366068

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f39d872f189b'
down_revision: Union[str, None] = '6465ad9e9f58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
