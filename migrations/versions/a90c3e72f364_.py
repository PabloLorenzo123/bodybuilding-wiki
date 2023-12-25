"""empty message

Revision ID: a90c3e72f364
Revises: 7e9e7ab31df1
Create Date: 2023-12-25 16:08:19.048336

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a90c3e72f364'
down_revision = '7e9e7ab31df1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('PapersSaved',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(length=300), nullable=True),
    sa.Column('authors', sa.String(length=300), nullable=True),
    sa.Column('pmid', sa.Integer(), nullable=True),
    sa.Column('abstract', sa.Text(), nullable=True),
    sa.Column('results', sa.Text(), nullable=True),
    sa.Column('conclusions', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('PapersSaved')
    # ### end Alembic commands ###