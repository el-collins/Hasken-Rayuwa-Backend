"""modified discipleship talble model

Revision ID: 5eadda5d4b52
Revises: 5c5777125a5d
Create Date: 2024-08-25 17:16:57.663321

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5eadda5d4b52'
down_revision: Union[str, None] = '5c5777125a5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_discipleship_reports_Month', table_name='discipleship_reports')
    op.drop_table('discipleship_reports')
    op.drop_table('film_show_reports')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('film_show_reports',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('Team', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('State', postgresql.ENUM('Abia', 'Adamawa', 'AkwaIbom', 'Anambra', 'Bauchi', 'Bayelsa', 'Benue', 'Borno', 'Cross_River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu', 'FCT', 'Gombe', 'Imo', 'Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos', 'Nasarawa', 'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo', 'Plateau', 'Rivers', 'Sokoto', 'Taraba', 'Yobe', 'Zamfara', name='states'), autoincrement=False, nullable=False),
    sa.Column('Ward', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('Village', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('LGA', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('Population', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('UPG', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('Attendance', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('SD_Cards', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('Audio_Bibles', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('People_Saved', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('Date', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('Month', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='film_show_reports_pkey')
    )
    op.create_table('discipleship_reports',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('Month', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('State', postgresql.ENUM('Abia', 'Adamawa', 'AkwaIbom', 'Anambra', 'Bauchi', 'Bayelsa', 'Benue', 'Borno', 'Cross_River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu', 'FCT', 'Gombe', 'Imo', 'Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos', 'Nasarawa', 'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo', 'Plateau', 'Rivers', 'Sokoto', 'Taraba', 'Yobe', 'Zamfara', name='states'), autoincrement=False, nullable=False),
    sa.Column('LGA', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('Ward', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('Village', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('Team', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('Population', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('UPG', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('Attendance', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('SD_Cards', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='discipleship_reports_pkey')
    )
    op.create_index('ix_discipleship_reports_Month', 'discipleship_reports', ['Month'], unique=False)
    # ### end Alembic commands ###
