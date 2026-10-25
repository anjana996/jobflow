"""Create Job, Profile and Preferences tables."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20261025_01"
down_revision = None
branch_labels = None
depends_on = None


def timestamp_columns() -> list[sa.Column]:
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    ]


def upgrade() -> None:
    op.create_table(
        "jobs",
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("company", sa.String(length=255), nullable=False),
        sa.Column("location", sa.String(length=255)),
        sa.Column("description", sa.Text()),
        sa.Column("canonical_url", sa.Text()),
        sa.Column("source", sa.String(length=100)),
        sa.Column("external_job_id", sa.String(length=255)),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        *timestamp_columns(),
        sa.PrimaryKeyConstraint("id", name="pk_jobs"),
        sa.UniqueConstraint("source", "external_job_id", name="uq_jobs_source_external_id"),
    )
    op.create_table(
        "profiles",
        sa.Column("full_name", sa.String(length=255)),
        sa.Column("email", sa.String(length=320)),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        *timestamp_columns(),
        sa.PrimaryKeyConstraint("id", name="pk_profiles"),
    )
    op.create_table(
        "preferences",
        sa.Column("profile_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("remote_only", sa.Boolean(), nullable=False),
        sa.Column("target_titles", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("target_locations", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        *timestamp_columns(),
        sa.ForeignKeyConstraint(
            ["profile_id"], ["profiles.id"], name="fk_preferences_profile_id_profiles", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_preferences"),
        sa.UniqueConstraint("profile_id", name="uq_preferences_profile_id"),
    )


def downgrade() -> None:
    op.drop_table("preferences")
    op.drop_table("profiles")
    op.drop_table("jobs")
