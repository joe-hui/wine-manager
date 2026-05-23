"""empty message

Revision ID: 0001
Revises:
Create Date: 2026-05-23 01:48:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "wineries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("country", sa.String(), nullable=False),
        sa.Column("region", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_wineries_id"), "wineries", ["id"])
    op.create_index(op.f("ix_wineries_name"), "wineries", ["name"], unique=True)

    op.create_table(
        "wines",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("winery_id", sa.Integer(), sa.ForeignKey("wineries.id"), nullable=False),
        sa.Column("type", sa.Enum("red", "white", "rose", "sparkling", "dessert", "fortified", name="winetype"), nullable=False),
        sa.Column("vintage", sa.Integer(), nullable=True),
        sa.Column("price", sa.Float(), nullable=True),
        sa.Column("abv", sa.Float(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_wines_id"), "wines", ["id"])
    op.create_index(op.f("ix_wines_name"), "wines", ["name"])

    op.create_table(
        "tasting_notes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("wine_id", sa.Integer(), sa.ForeignKey("wines.id"), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("tasted_on", sa.Date(), nullable=False),
        sa.Column("reviewer", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tasting_notes_id"), "tasting_notes", ["id"])


def downgrade() -> None:
    op.drop_table("tasting_notes")
    op.drop_table("wines")
    op.drop_table("wineries")
