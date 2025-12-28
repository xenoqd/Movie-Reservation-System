"""add status column to reservation model

Revision ID: b043aa21bbc0
Revises: 027bed7370e8
Create Date: 2025-12-28 13:44:18.615843

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b043aa21bbc0'
down_revision: Union[str, None] = '027bed7370e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    reservationstatus = sa.Enum('ACTIVE', 'CANCELLED', 'EXPIRED', name='reservationstatus')
    reservationstatus.create(op.get_bind(), checkfirst=True)

    op.add_column(
        'reservation',
        sa.Column('status', reservationstatus, nullable=False, server_default='ACTIVE')
    )

def downgrade() -> None:
    op.drop_column('reservation', 'status')

    reservationstatus = sa.Enum('ACTIVE', 'CANCELLED', 'EXPIRED', name='reservationstatus')
    reservationstatus.drop(op.get_bind(), checkfirst=True)