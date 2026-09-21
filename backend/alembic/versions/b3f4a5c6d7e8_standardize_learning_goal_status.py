"""standardize learning_goals.status to ACTIVE

Revision ID: b3f4a5c6d7e8
Revises: a1b2c3d4e5f6
Create Date: 2026-09-21 19:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3f4a5c6d7e8'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Backfill existing goals to 'ACTIVE' and align the column default."""
    op.execute(
        "UPDATE learning_goals SET status = 'ACTIVE' "
        "WHERE status = 'in_progress'"
    )
    op.alter_column(
        'learning_goals',
        'status',
        server_default='ACTIVE',
        existing_type=sa.String(length=30),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Restore the previous default; converted rows are not rolled back."""
    op.alter_column(
        'learning_goals',
        'status',
        server_default='in_progress',
        existing_type=sa.String(length=30),
        existing_nullable=False,
    )