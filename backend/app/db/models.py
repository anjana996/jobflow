"""Initial relational models for JobFlow."""

from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base, IdentityTimestampMixin


class Job(IdentityTimestampMixin, Base):
    """A job listing saved manually or discovered from a configured source."""

    __tablename__ = "jobs"
    __table_args__ = (
        UniqueConstraint("source", "external_job_id", name="uq_jobs_source_external_id"),
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    company: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    canonical_url: Mapped[str | None] = mapped_column(Text)
    source: Mapped[str | None] = mapped_column(String(100))
    external_job_id: Mapped[str | None] = mapped_column(String(255))


class Profile(IdentityTimestampMixin, Base):
    """Verified facts about the single JobFlow owner."""

    __tablename__ = "profiles"

    full_name: Mapped[str | None] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(320))
    preferences: Mapped["Preferences | None"] = relationship(
        back_populates="profile", cascade="all, delete-orphan", uselist=False
    )


class Preferences(IdentityTimestampMixin, Base):
    """The owner's job-discovery rules; detailed behavior arrives in JF-10."""

    __tablename__ = "preferences"

    profile_id: Mapped[UUID] = mapped_column(
        ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    remote_only: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    target_titles: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    target_locations: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    profile: Mapped[Profile] = relationship(back_populates="preferences")
