"""add completed booking status

Revision ID: 8048ccc22663
Revises: 5ead272ff837
Create Date: 2026-09-01 22:37:13.370708

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8048ccc22663'
down_revision: Union[str, Sequence[str], None] = '5ead272ff837'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE bookingstatus ADD VALUE 'COMPLETED'")





def downgrade() -> None:
    """Downgrade schema."""
    pass
