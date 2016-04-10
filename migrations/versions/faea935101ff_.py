"""empty message

Revision ID: faea935101ff
Revises: 0866d9c9eb2e
Create Date: 2016-04-09 17:06:25.718429

"""

# revision identifiers, used by Alembic.
revision = 'faea935101ff'
down_revision = '0866d9c9eb2e'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'date_modified')
    op.drop_column('users', 'date_added')
    op.drop_column('users', 'is_admin')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_admin', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('date_added', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('date_modified', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('is_active', sa.INTEGER(), autoincrement=False, nullable=True))
    ### end Alembic commands ###
