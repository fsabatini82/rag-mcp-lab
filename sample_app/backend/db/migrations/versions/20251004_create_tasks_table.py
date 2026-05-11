"""create tasks table — baseline migration.

Revision ID: 20251004_create_tasks_table
Revises:
Create Date: 2025-10-04
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20251004_create_tasks_table"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("project_id", sa.UUID(), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.String(5000), nullable=False, server_default=""),
        sa.Column("status", sa.String(20), nullable=False, server_default="open"),
        sa.Column("assignee_id", sa.UUID(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("idx_tasks_project_id", "tasks", ["project_id"])


def downgrade() -> None:
    op.drop_index("idx_tasks_project_id", "tasks")
    op.drop_table("tasks")
