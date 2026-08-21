"""add_users_table_and_user_id_fk

Revision ID: 32e9288b7112
Revises: 8999090bfdd4
Create Date: 2026-08-15 16:52:06.219861

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '32e9288b7112'
down_revision: Union[str, Sequence[str], None] = '8999090bfdd4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    with op.batch_alter_table('urls', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_urls_users_id', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    with op.batch_alter_table('urls', schema=None) as batch_op:
        batch_op.drop_constraint('fk_urls_users_id', type_='foreignkey')
        batch_op.drop_column('user_id')

    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
