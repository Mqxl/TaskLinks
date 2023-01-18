"""empty message

Revision ID: babad5f8dc4c
Revises: 57951b56149a
Create Date: 2023-01-15 20:46:50.604267

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'babad5f8dc4c'
down_revision = '57951b56149a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('links',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('link', sa.String(length=255), nullable=False),
    sa.Column('click_cost', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_links_click_cost'), 'links', ['click_cost'], unique=False)
    op.create_index(op.f('ix_links_link'), 'links', ['link'], unique=True)
    op.create_table('clicks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('link_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['link_id'], ['links.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('views',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('link_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['link_id'], ['links.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_points_name', 'points', ['name'], unique=False)
    op.drop_table('views')
    op.drop_table('clicks')
    op.drop_index(op.f('ix_links_link'), table_name='links')
    op.drop_index(op.f('ix_links_click_cost'), table_name='links')
    op.drop_table('links')
    # ### end Alembic commands ###
