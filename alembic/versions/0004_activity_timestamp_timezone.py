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


def _alter_last_xp_at(*, downgrade: bool = False) -> None:
    bind = op.get_bind()
    if bind.dialect.name == "sqlite":
        with op.batch_alter_table("chat_members", recreate="always") as batch_op:
            batch_op.alter_column(
                "last_xp_at",
                existing_type=sa.DateTime(timezone=not downgrade),
                type_=sa.DateTime(timezone=downgrade),
                existing_nullable=True,
            )
        return

    if downgrade:
        op.alter_column(
            "chat_members",
            "last_xp_at",
            existing_type=sa.DateTime(timezone=True),
            type_=sa.DateTime(),
            existing_nullable=True,
            postgresql_using="last_xp_at AT TIME ZONE 'UTC'",
        )
        return

    op.alter_column(
        "chat_members",
        "last_xp_at",
        existing_type=sa.DateTime(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=True,
        postgresql_using="last_xp_at AT TIME ZONE 'UTC'",
    )


def upgrade() -> None:
    _alter_last_xp_at()


def downgrade() -> None:
    _alter_last_xp_at(downgrade=True)
