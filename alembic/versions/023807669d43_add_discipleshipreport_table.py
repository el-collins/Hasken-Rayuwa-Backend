"""Add DiscipleshipReport table

Revision ID: 023807669d43
Revises: 8a1658b7e948
Create Date: 2024-08-15 09:04:14.547007

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '023807669d43'
down_revision: Union[str, None] = '8a1658b7e948'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_discipleship_reports_lga', table_name='discipleship_reports')
    op.drop_index('ix_discipleship_reports_month', table_name='discipleship_reports')
    op.drop_table('discipleship_reports')
    op.drop_index('ix_film_show_reports_lga', table_name='film_show_reports')
    op.drop_index('ix_film_show_reports_month', table_name='film_show_reports')
    op.drop_table('film_show_reports')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('film_show_reports',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('month', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('state', postgresql.ENUM('Abia', 'Adamawa', 'AkwaIbom', 'Anambra', 'Bauchi', 'Bayelsa', 'Benue', 'Borno', 'Cross_River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu', 'FCT', 'Gombe', 'Imo', 'Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos', 'Nasarawa', 'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo', 'Plateau', 'Rivers', 'Sokoto', 'Taraba', 'Yobe', 'Zamfara', name='states'), autoincrement=False, nullable=False),
    sa.Column('lga', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('wards', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('village', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('team', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('population', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('upg', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('attendance', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('sd_cards', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('audio_bibles', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('people_saved', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='film_show_reports_pkey')
    )
    op.create_index('ix_film_show_reports_month', 'film_show_reports', ['month'], unique=False)
    op.create_index('ix_film_show_reports_lga', 'film_show_reports', ['lga'], unique=False)
    op.create_table('discipleship_reports',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('month', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('state', postgresql.ENUM('Abia', 'Adamawa', 'AkwaIbom', 'Anambra', 'Bauchi', 'Bayelsa', 'Benue', 'Borno', 'Cross_River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu', 'FCT', 'Gombe', 'Imo', 'Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos', 'Nasarawa', 'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo', 'Plateau', 'Rivers', 'Sokoto', 'Taraba', 'Yobe', 'Zamfara', name='states'), autoincrement=False, nullable=False),
    sa.Column('lga', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('wards', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('village', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('team', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('population', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('upg', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('attendance', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('sdc_given', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='discipleship_reports_pkey')
    )
    op.create_index('ix_discipleship_reports_month', 'discipleship_reports', ['month'], unique=False)
    op.create_index('ix_discipleship_reports_lga', 'discipleship_reports', ['lga'], unique=False)
    # ### end Alembic commands ###