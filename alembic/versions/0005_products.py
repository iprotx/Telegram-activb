"""Add KEYDROP catalog products.

Revision ID: 0005_products
Revises: 0004_activity_timestamp_timezone
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0005_products"
down_revision: str | None = "0004_activity_timestamp_timezone"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("provider_product_id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.String(length=500), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("description_html", sa.Text(), nullable=True),
        sa.Column("price_kopeks", sa.BigInteger(), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("stock", sa.Integer(), nullable=True),
        sa.Column("stock_unlimited", sa.Boolean(), nullable=False),
        sa.Column("available", sa.Boolean(), nullable=False),
        sa.Column("category", sa.String(length=255), nullable=True),
        sa.Column("synced_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("provider_product_id"),
    )
    op.create_index("ix_products_provider_product_id", "products", ["provider_product_id"])
    op.create_index("ix_products_available", "products", ["available"])
    op.create_index("ix_products_category", "products", ["category"])


def downgrade() -> None:
    op.drop_index("ix_products_category", table_name="products")
    op.drop_index("ix_products_available", table_name="products")
    op.drop_index("ix_products_provider_product_id", table_name="products")
    op.drop_table("products")
