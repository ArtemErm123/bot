from __future__ import annotations

from datetime import date
from typing import Optional

from sqlalchemy import (
    JSON,
    Boolean,
    Date,
    Float,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Role(TimestampMixin, Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)

    users: Mapped[list["User"]] = relationship(back_populates="role")


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    role: Mapped[Role] = relationship(back_populates="users")
    project_memberships: Mapped[list["ProjectMember"]] = relationship(back_populates="user")


class Project(TimestampMixin, Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    members: Mapped[list["ProjectMember"]] = relationship(back_populates="project")
    variants: Mapped[list["Variant"]] = relationship(back_populates="project")


class ProjectMember(TimestampMixin, Base):
    __tablename__ = "project_members"
    __table_args__ = (UniqueConstraint("project_id", "user_id", name="uq_project_member"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    project_role: Mapped[str] = mapped_column(String(100), nullable=False)

    project: Mapped[Project] = relationship(back_populates="members")
    user: Mapped[User] = relationship(back_populates="project_memberships")


class Variant(TimestampMixin, Base):
    __tablename__ = "variants"
    __table_args__ = (UniqueConstraint("project_id", "name", name="uq_project_variant_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft")

    project: Mapped[Project] = relationship(back_populates="variants")
    layers: Mapped[list["Layer"]] = relationship(back_populates="variant")


class Layer(TimestampMixin, Base):
    __tablename__ = "layers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    variant_id: Mapped[int] = mapped_column(ForeignKey("variants.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    thickness_mm: Mapped[float] = mapped_column(Float, nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    variant: Mapped[Variant] = relationship(back_populates="layers")


class Material(TimestampMixin, Base):
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    supplier: Mapped[Optional[str]] = mapped_column(String(255))

    properties: Mapped[list["MaterialProperty"]] = relationship(back_populates="material")


class MaterialProperty(TimestampMixin, Base):
    __tablename__ = "material_properties"
    __table_args__ = (
        UniqueConstraint("material_id", "property_name", name="uq_material_property"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id"), nullable=False)
    property_name: Mapped[str] = mapped_column(String(100), nullable=False)
    property_value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[Optional[str]] = mapped_column(String(50))

    material: Mapped[Material] = relationship(back_populates="properties")


class Mix(TimestampMixin, Base):
    __tablename__ = "mixes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    current_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    components: Mapped[list["MixComponent"]] = relationship(back_populates="mix")
    gradation_points: Mapped[list["GradationPoint"]] = relationship(back_populates="mix")
    passports: Mapped[list["MixPassport"]] = relationship(back_populates="mix")
    versions: Mapped[list["MixVersion"]] = relationship(back_populates="mix")


class MixVersion(TimestampMixin, Base):
    __tablename__ = "mix_versions"
    __table_args__ = (
        UniqueConstraint("mix_id", "version", name="uq_mix_version"),
        Index("ix_mix_versions_mix_id_version", "mix_id", "version"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mix_id: Mapped[int] = mapped_column(ForeignKey("mixes.id"), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    change_note: Mapped[Optional[str]] = mapped_column(Text)
    changed_by_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    snapshot: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    mix: Mapped[Mix] = relationship(back_populates="versions")


class MixComponent(TimestampMixin, Base):
    __tablename__ = "mix_components"
    __table_args__ = (
        UniqueConstraint("mix_id", "material_id", name="uq_mix_component_material"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mix_id: Mapped[int] = mapped_column(ForeignKey("mixes.id"), nullable=False)
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id"), nullable=False)
    percent: Mapped[float] = mapped_column(Float, nullable=False)

    mix: Mapped[Mix] = relationship(back_populates="components")


class GradationPoint(TimestampMixin, Base):
    __tablename__ = "gradation_points"
    __table_args__ = (
        UniqueConstraint("mix_id", "sieve_mm", name="uq_mix_sieve"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mix_id: Mapped[int] = mapped_column(ForeignKey("mixes.id"), nullable=False)
    sieve_mm: Mapped[float] = mapped_column(Float, nullable=False)
    passing_percent: Mapped[float] = mapped_column(Float, nullable=False)

    mix: Mapped[Mix] = relationship(back_populates="gradation_points")


class MixPassport(TimestampMixin, Base):
    __tablename__ = "mix_passports"
    __table_args__ = (
        UniqueConstraint("mix_id", "version", name="uq_mix_passport_version"),
        Index("ix_mix_passports_mix_id_version", "mix_id", "version"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mix_id: Mapped[int] = mapped_column(ForeignKey("mixes.id"), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    valid_from: Mapped[date] = mapped_column(Date, nullable=False)
    valid_to: Mapped[Optional[date]] = mapped_column(Date)
    previous_passport_id: Mapped[Optional[int]] = mapped_column(ForeignKey("mix_passports.id"))
    is_current: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    change_note: Mapped[Optional[str]] = mapped_column(Text)

    mix: Mapped[Mix] = relationship(back_populates="passports")


class Calculation(TimestampMixin, Base):
    __tablename__ = "calculations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mix_id: Mapped[int] = mapped_column(ForeignKey("mixes.id"), nullable=False)
    variant_id: Mapped[int] = mapped_column(ForeignKey("variants.id"), nullable=False)
    parameters: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="queued")

    scenarios: Mapped[list["Scenario"]] = relationship(back_populates="calculation")


class Scenario(TimestampMixin, Base):
    __tablename__ = "scenarios"
    __table_args__ = (
        UniqueConstraint("calculation_id", "name", name="uq_calculation_scenario_name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    calculation_id: Mapped[int] = mapped_column(ForeignKey("calculations.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    calculation: Mapped[Calculation] = relationship(back_populates="scenarios")
    predictions: Mapped[list["Prediction"]] = relationship(back_populates="scenario")


class Prediction(TimestampMixin, Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scenario_id: Mapped[int] = mapped_column(ForeignKey("scenarios.id"), nullable=False)
    model_name: Mapped[str] = mapped_column(String(255), nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    result_payload: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    scenario: Mapped[Scenario] = relationship(back_populates="predictions")
    reports: Mapped[list["Report"]] = relationship(back_populates="prediction")


class Report(TimestampMixin, Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    prediction_id: Mapped[int] = mapped_column(ForeignKey("predictions.id"), nullable=False)
    format: Mapped[str] = mapped_column(String(20), nullable=False)
    location: Mapped[str] = mapped_column(String(1024), nullable=False)
    checksum: Mapped[Optional[str]] = mapped_column(String(128))

    prediction: Mapped[Prediction] = relationship(back_populates="reports")
