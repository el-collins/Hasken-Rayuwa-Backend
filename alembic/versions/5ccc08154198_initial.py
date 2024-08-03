"""Initial

Revision ID: 5ccc08154198
Revises: 1357e8261498
Create Date: 2024-08-03 08:23:56.387215

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ccc08154198'
down_revision: Union[str, None] = '1357e8261498'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
