"""empty message

Revision ID: b5552a037c91
Revises: 
Create Date: 2023-02-03 16:04:30.082272

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5552a037c91'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('wallet',
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('payment_page_slug', sa.String(), nullable=False),
    sa.Column('payment_page_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('address'),
    sa.UniqueConstraint('payment_page_id'),
    sa.UniqueConstraint('payment_page_slug')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wallet')
    # ### end Alembic commands ###
