"""empty message

Revision ID: 523c6bf26201
Revises: faea935101ff
Create Date: 2016-04-09 17:25:03.245104

"""

# revision identifiers, used by Alembic.
revision = '523c6bf26201'
down_revision = 'faea935101ff'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('date_added', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('date_modified', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('is_active', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('is_admin', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_admin')
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'date_modified')
    op.drop_column('users', 'date_added')
    ### end Alembic commands ###
