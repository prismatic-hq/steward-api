"""add work order source alert

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-27
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: str | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SCHEMA = "steward"
CONSTRAINT = "uq_work_orders_source_alert_id"


def upgrade() -> None:
    op.add_column(
        "work_orders", sa.Column("source_alert_id", sa.Uuid(), nullable=True), schema=SCHEMA
    )
    op.create_unique_constraint(CONSTRAINT, "work_orders", ["source_alert_id"], schema=SCHEMA)


def downgrade() -> None:
    op.drop_constraint(CONSTRAINT, "work_orders", schema=SCHEMA, type_="unique")
    op.drop_column("work_orders", "source_alert_id", schema=SCHEMA)
