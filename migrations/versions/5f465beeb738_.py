"""empty message

Revision ID: 5f465beeb738
Revises: 24ff9a868bcf
Create Date: 2023-04-16 19:20:58.016148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f465beeb738'
down_revision = '24ff9a868bcf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('games_played', sa.Integer(), server_default='0', nullable=False))
        batch_op.add_column(sa.Column('games_won', sa.Integer(), server_default='0', nullable=False))
        batch_op.add_column(sa.Column('earned_points', sa.Integer(), server_default='0', nullable=False))
        batch_op.add_column(sa.Column('spent_points', sa.Integer(), server_default='0', nullable=False))
        batch_op.add_column(sa.Column('words_composed', sa.Integer(), server_default='0', nullable=False))
        batch_op.add_column(sa.Column('players_killed', sa.Integer(), server_default='0', nullable=False))
        batch_op.alter_column('pass',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.create_unique_constraint(None, ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('pass',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.drop_column('players_killed')
        batch_op.drop_column('words_composed')
        batch_op.drop_column('spent_points')
        batch_op.drop_column('earned_points')
        batch_op.drop_column('games_won')
        batch_op.drop_column('games_played')

    # ### end Alembic commands ###