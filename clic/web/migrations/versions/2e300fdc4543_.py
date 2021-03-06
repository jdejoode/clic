"""empty message

Revision ID: 2e300fdc4543
Revises: 37ed83d4e343
Create Date: 2015-11-05 18:23:48.098750

"""

# revision identifiers, used by Alembic.
revision = '2e300fdc4543'
down_revision = '37ed83d4e343'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('name', sa.String(length=35), nullable=True))
    op.create_unique_constraint(None, 'user', ['name'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'name')
    ### end Alembic commands ###
