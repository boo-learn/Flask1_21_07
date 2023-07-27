"""add rate

Revision ID: f07a04a2ffcf
Revises: 885796e25578
Create Date: 2023-07-27 23:59:10.070902

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f07a04a2ffcf'
down_revision = '885796e25578'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quote_model', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rate', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('quote_model', schema=None) as batch_op:
        batch_op.drop_column('rate')

    # ### end Alembic commands ###