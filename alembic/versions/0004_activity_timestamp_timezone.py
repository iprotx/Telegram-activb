"""Store activity XP timestamps as timezone-aware UTC instants.

Revision ID: 0004_activity_timestamp_timezone
Revises: 0003_chat_telegram_id_constraint
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0004_activity_timestamp_timezone"
down_revision: str | None = "0003_chat_telegram_id_constraint"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        "chat_members",
        "last_xp_at",
        existing_type=sa.DateTime(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=True,
        postgresql_using="last_xp_at AT TIME ZONE 'UTC'",
    )


def downgrade() -> None:
    op.alter_column(
        "chat_members",
        "last_xp_at",
        existing_type=sa.DateTime(timezone=True),
        type_=sa.DateTime(),
        existing_nullable=True,
        postgresql_using="last_xp_at AT TIME ZONE 'UTC'",
    )
