"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-02-17 00:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0001_initial"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("name", name="uq_roles_name"),
    )
    op.create_index("ix_roles_name", "roles", ["name"], unique=False)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], name="fk_users_role_id_roles"),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=False)

    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"], name="fk_projects_owner_id_users"),
        sa.UniqueConstraint("code", name="uq_projects_code"),
    )

    op.create_table(
        "materials",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("supplier", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("name", name="uq_materials_name"),
    )

    op.create_table(
        "mixes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("current_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("is_archived", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("code", name="uq_mixes_code"),
    )

    op.create_table(
        "material_properties",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("material_id", sa.Integer(), nullable=False),
        sa.Column("property_name", sa.String(length=100), nullable=False),
        sa.Column("property_value", sa.Float(), nullable=False),
        sa.Column("unit", sa.String(length=50), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["material_id"], ["materials.id"], name="fk_material_properties_material_id_materials"),
        sa.UniqueConstraint("material_id", "property_name", name="uq_material_property"),
    )

    op.create_table(
        "mix_versions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("mix_id", sa.Integer(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("change_note", sa.Text(), nullable=True),
        sa.Column("changed_by_id", sa.Integer(), nullable=True),
        sa.Column("snapshot", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["changed_by_id"], ["users.id"], name="fk_mix_versions_changed_by_id_users"),
        sa.ForeignKeyConstraint(["mix_id"], ["mixes.id"], name="fk_mix_versions_mix_id_mixes"),
        sa.UniqueConstraint("mix_id", "version", name="uq_mix_version"),
    )
    op.create_index("ix_mix_versions_mix_id_version", "mix_versions", ["mix_id", "version"], unique=False)

    op.create_table(
        "variants",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="draft"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], name="fk_variants_project_id_projects"),
        sa.UniqueConstraint("project_id", "name", name="uq_project_variant_name"),
    )

    op.create_table(
        "project_members",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("project_role", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], name="fk_project_members_project_id_projects"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_project_members_user_id_users"),
        sa.UniqueConstraint("project_id", "user_id", name="uq_project_member"),
    )

    op.create_table(
        "layers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("variant_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("thickness_mm", sa.Float(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["variant_id"], ["variants.id"], name="fk_layers_variant_id_variants"),
    )

    op.create_table(
        "mix_components",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("mix_id", sa.Integer(), nullable=False),
        sa.Column("material_id", sa.Integer(), nullable=False),
        sa.Column("percent", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["material_id"], ["materials.id"], name="fk_mix_components_material_id_materials"),
        sa.ForeignKeyConstraint(["mix_id"], ["mixes.id"], name="fk_mix_components_mix_id_mixes"),
        sa.UniqueConstraint("mix_id", "material_id", name="uq_mix_component_material"),
    )

    op.create_table(
        "gradation_points",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("mix_id", sa.Integer(), nullable=False),
        sa.Column("sieve_mm", sa.Float(), nullable=False),
        sa.Column("passing_percent", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["mix_id"], ["mixes.id"], name="fk_gradation_points_mix_id_mixes"),
        sa.UniqueConstraint("mix_id", "sieve_mm", name="uq_mix_sieve"),
    )

    op.create_table(
        "mix_passports",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("mix_id", sa.Integer(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("valid_from", sa.Date(), nullable=False),
        sa.Column("valid_to", sa.Date(), nullable=True),
        sa.Column("previous_passport_id", sa.Integer(), nullable=True),
        sa.Column("is_current", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("change_note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["mix_id"], ["mixes.id"], name="fk_mix_passports_mix_id_mixes"),
        sa.ForeignKeyConstraint(["previous_passport_id"], ["mix_passports.id"], name="fk_mix_passports_previous_passport_id_mix_passports"),
        sa.UniqueConstraint("mix_id", "version", name="uq_mix_passport_version"),
    )
    op.create_index("ix_mix_passports_mix_id_version", "mix_passports", ["mix_id", "version"], unique=False)

    op.create_table(
        "calculations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("mix_id", sa.Integer(), nullable=False),
        sa.Column("variant_id", sa.Integer(), nullable=False),
        sa.Column("parameters", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="queued"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["mix_id"], ["mixes.id"], name="fk_calculations_mix_id_mixes"),
        sa.ForeignKeyConstraint(["variant_id"], ["variants.id"], name="fk_calculations_variant_id_variants"),
    )

    op.create_table(
        "scenarios",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("calculation_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["calculation_id"], ["calculations.id"], name="fk_scenarios_calculation_id_calculations"),
        sa.UniqueConstraint("calculation_id", "name", name="uq_calculation_scenario_name"),
    )

    op.create_table(
        "predictions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("scenario_id", sa.Integer(), nullable=False),
        sa.Column("model_name", sa.String(length=255), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("result_payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["scenario_id"], ["scenarios.id"], name="fk_predictions_scenario_id_scenarios"),
    )

    op.create_table(
        "reports",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("prediction_id", sa.Integer(), nullable=False),
        sa.Column("format", sa.String(length=20), nullable=False),
        sa.Column("location", sa.String(length=1024), nullable=False),
        sa.Column("checksum", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["prediction_id"], ["predictions.id"], name="fk_reports_prediction_id_predictions"),
    )


def downgrade() -> None:
    op.drop_table("reports")
    op.drop_table("predictions")
    op.drop_table("scenarios")
    op.drop_table("calculations")
    op.drop_index("ix_mix_passports_mix_id_version", table_name="mix_passports")
    op.drop_table("mix_passports")
    op.drop_table("gradation_points")
    op.drop_table("mix_components")
    op.drop_table("layers")
    op.drop_table("project_members")
    op.drop_table("variants")
    op.drop_index("ix_mix_versions_mix_id_version", table_name="mix_versions")
    op.drop_table("mix_versions")
    op.drop_table("material_properties")
    op.drop_table("mixes")
    op.drop_table("materials")
    op.drop_table("projects")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
    op.drop_index("ix_roles_name", table_name="roles")
    op.drop_table("roles")
