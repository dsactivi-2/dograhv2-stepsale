"""merge alembic heads: training modules + org model config backfill

Revision ID: f8a9b0c1d2e3
Revises: e4f5a6b7c8d9, 00b0201ad918
Create Date: 2026-07-30 02:00:00.000000

"""

from typing import Sequence, Union

revision: str = "f8a9b0c1d2e3"
down_revision: Union[str, Sequence[str], None] = ("e4f5a6b7c8d9", "00b0201ad918")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
