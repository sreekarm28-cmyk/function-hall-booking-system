"""add completed booking status

Revision ID: 5ead272ff837
Revises: c7819dde27cf
Create Date: 2026-09-01 22:34:52.465558

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ead272ff837'
down_revision: Union[str, Sequence[str], None] = 'c7819dde27cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
