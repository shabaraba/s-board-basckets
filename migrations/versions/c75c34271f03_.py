"""empty message

Revision ID: c75c34271f03
Revises: 4fd23444e08e
Create Date: 2020-11-19 08:38:14.174642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c75c34271f03'
down_revision = '4fd23444e08e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('diaries2')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('diaries2',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('date', sa.VARCHAR(length=255), nullable=True),
    sa.Column('book_title', sa.VARCHAR(length=255), nullable=True),
    sa.Column('impression', sa.TEXT(), nullable=True),
    sa.Column('deleted', sa.BOOLEAN(), nullable=True),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.CheckConstraint('deleted IN (0, 1)'),
    sa.ForeignKeyConstraint(['book_title'], ['books.title'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###