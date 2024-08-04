"""Recreated missing revision

Revision ID: 68151a0c483d
Revises: 5ccc08154198
Create Date: 2024-08-04 23:43:28.004895

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '68151a0c483d'
down_revision: Union[str, None] = '5ccc08154198'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_state_data_Lga', table_name='state_data')
    op.drop_table('state_data')
    op.drop_table('users')
    op.drop_table('volunteer')
    op.drop_index('ix_links_media_type', table_name='links')
    op.drop_index('ix_links_url', table_name='links')
    op.drop_table('links')
    op.drop_table('blogs')
    op.drop_table('contact')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contact',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('fullname', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('contact_email', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('message', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='contact_pkey')
    )
    op.create_table('blogs',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('content', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('visibility', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='blogs_pkey')
    )
    op.create_table('links',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('media_type', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='links_pkey')
    )
    op.create_index('ix_links_url', 'links', ['url'], unique=True)
    op.create_index('ix_links_media_type', 'links', ['media_type'], unique=False)
    op.create_table('volunteer',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('fullname', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('volunteer_email', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('phone_number', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('address', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='volunteer_pkey')
    )
    op.create_table('users',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('fullname', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('email', sa.TEXT(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='users_pkey'),
    sa.UniqueConstraint('email', name='users_email_key')
    )
    op.create_table('state_data',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('State', postgresql.ENUM('Abia', 'Adamawa', 'AkwaIbom', 'Anambra', 'Bauchi', 'Bayelsa', 'Benue', 'Borno', 'Cross_River', 'Delta', 'Ebonyi', 'Edo', 'Ekiti', 'Enugu', 'FCT', 'Gombe', 'Imo', 'Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos', 'Nasarawa', 'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo', 'Plateau', 'Rivers', 'Sokoto', 'Taraba', 'Yobe', 'Zamfara', name='states'), autoincrement=False, nullable=False),
    sa.Column('Lga', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('Ward', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('Village', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('Estimated_Christian_Population', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Estimated_Muslim_Population', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Estimated_Traditional_Religion_Population', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Converts', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Estimated_Total_Population', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Film_Attendance', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('People_Group', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('Practiced_Religion', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='state_data_pkey')
    )
    op.create_index('ix_state_data_Lga', 'state_data', ['Lga'], unique=False)
    # ### end Alembic commands ###
