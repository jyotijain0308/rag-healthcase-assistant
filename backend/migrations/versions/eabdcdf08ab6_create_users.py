"""create_users

Revision ID: eabdcdf08ab6
Revises: 034a36665cb9
Create Date: 2026-05-14 17:48:15.874931

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'eabdcdf08ab6'
down_revision: Union[str, Sequence[str], None] = '034a36665cb9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',

        sa.Column(
            'id',
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            'username',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'email',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'hashed_password',
            sa.String(),
            nullable=False
        ),

        sa.Column(
            'role',
            sa.String(),
            nullable=False
        ),

        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('users')
