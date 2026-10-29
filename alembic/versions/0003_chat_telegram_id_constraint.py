"""Normalize chats.telegram_id uniqueness for databases migrated by older 0002 revisions.

Revision ID: 0003_chat_telegram_id_constraint
Revises: 0002_activity
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0003_chat_telegram_id_constraint"
down_revision: str | None = "0002_activity"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Converge older unique-index schemas and fresh constraint schemas."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    indexes = {index["name"]: index for index in inspector.get_indexes("chats")}
    unique_constraints = {
        constraint["name"]: constraint for constraint in inspector.get_unique_constraints("chats")
    }

    constraint_name = "uq_chats_telegram_id"
    index_name = "ix_chats_telegram_id"

    if index_name in indexes:
        op.drop_index(index_name, table_name="chats")

    has_expected_constraint = any(
        constraint.get("name") == constraint_name
        and constraint.get("column_names") == ["telegram_id"]
        for constraint in unique_constraints.values()
    )
    if not has_expected_constraint:
        op.create_unique_constraint(
            constraint_name,
            "chats",
            ["telegram_id"],
        )


def downgrade() -> None:
    """Keep the canonical schema required by 0002_activity.

    This migration is a compatibility repair for databases where an earlier
    version of 0002_activity created a standalone unique index. Reverting the
    repair would reintroduce drift against the current 0002_activity revision.
    """
