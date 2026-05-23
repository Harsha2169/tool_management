"""create tooling tables

Revision ID: 001_initial
Revises:
Create Date: 2026-05-21

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Tool Type Lookup
    op.create_table(
        "tool_type_lookup",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("type_name", sa.String(50), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("type_name"),
    )

    # Tool Master
    op.create_table(
        "tool_master",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("tool_id", sa.String(50), nullable=False),
        sa.Column("tool_description", sa.String(255), nullable=False),
        sa.Column("tool_type_id", sa.BigInteger(), nullable=False),
        sa.Column("life_status", sa.String(20), nullable=False, server_default="Active"),
        sa.Column("make", sa.String(100), nullable=True),
        sa.Column("model", sa.String(100), nullable=True),
        sa.Column("asset_owner", sa.String(50), nullable=False),
        sa.Column("acquired_date", sa.Date(), nullable=True),
        sa.Column("lifecycle_limit", sa.BigInteger(), nullable=False),
        sa.Column("control_unit", sa.String(50), nullable=False),
        sa.Column("lifecycle_initial_value", sa.BigInteger(), server_default=sa.text("0")),
        sa.Column("current_usage", sa.BigInteger(), server_default=sa.text("0")),
        sa.Column("plant_id", sa.String(50), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["tool_type_id"], ["tool_type_lookup.id"]),
        sa.UniqueConstraint("tool_id"),
    )
    op.create_index("ix_tool_master_tool_id", "tool_master", ["tool_id"])

    # Tool Production
    op.create_table(
        "tool_production",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("tool_master_id", sa.BigInteger(), nullable=False),
        sa.Column("tool_part_code", sa.String(50), nullable=False),
        sa.Column("cavities", sa.Integer(), nullable=False),
        sa.Column("cavity_numbers", sa.String(50), nullable=True),
        sa.Column("weight_all_parts_g", sa.Numeric(10, 2), nullable=True),
        sa.Column("weight_runner_g", sa.Numeric(10, 2), nullable=True),
        sa.Column("weight_shot_g", sa.Numeric(10, 2), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["tool_master_id"], ["tool_master.id"]),
    )

    # Tool Performance
    op.create_table(
        "tool_performance",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("tool_master_id", sa.BigInteger(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("performance_value", sa.Numeric(12, 2), nullable=True),
        sa.Column("cumulative", sa.Numeric(12, 2), nullable=True),
        sa.Column("uom", sa.String(50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["tool_master_id"], ["tool_master.id"]),
    )

    # Tool Params
    op.create_table(
        "tool_params",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("tool_master_id", sa.BigInteger(), nullable=False),
        sa.Column("parameter_name", sa.String(100), nullable=False),
        sa.Column("parameter_value", sa.String(100), nullable=False),
        sa.Column("uom", sa.String(50), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["tool_master_id"], ["tool_master.id"]),
    )

    # Tool Maintenance
    op.create_table(
        "tool_maintenance",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("tool_master_id", sa.BigInteger(), nullable=False),
        sa.Column("maintenance_date", sa.Date(), nullable=False),
        sa.Column("maintenance_type", sa.String(50), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("performed_by", sa.String(100), nullable=True),
        sa.Column("next_due_date", sa.Date(), nullable=True),
        sa.Column("cost", sa.Numeric(12, 2), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["tool_master_id"], ["tool_master.id"]),
    )

    # Seed tool types
    op.execute(
        "INSERT INTO tool_type_lookup (type_name, is_active) VALUES "
        "('Injection Mould', true), "
        "('CNC Tooling', true), "
        "('Die for Casting', true), "
        "('Die for Press', true)"
    )


def downgrade() -> None:
    op.drop_table("tool_maintenance")
    op.drop_table("tool_params")
    op.drop_table("tool_performance")
    op.drop_table("tool_production")
    op.drop_index("ix_tool_master_tool_id", table_name="tool_master")
    op.drop_table("tool_master")
    op.drop_table("tool_type_lookup")
