# app/models/tenant.py
from __future__ import annotations

from ..extensions import db
from .mixins import UUIDPrimaryKeyMixin, TimestampMixin


class Group(db.Model, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "groups"

    name = db.Column(db.String(255), nullable=False)
    owner_user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

    is_active = db.Column(db.Boolean, nullable=False, default=True)

    companies = db.relationship(
        "Company",
        back_populates="group",
        lazy="select",
        cascade="all, delete-orphan",
    )


class Company(db.Model, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "companies"

    group_id = db.Column(db.String(36), db.ForeignKey("groups.id"), nullable=False, index=True)

    name = db.Column(db.String(255), nullable=False)
    timezone = db.Column(db.String(50), nullable=False, default="America/Sao_Paulo")

    is_active = db.Column(db.Boolean, nullable=False, default=True)

    group = db.relationship("Group", back_populates="companies", lazy="select")

    users = db.relationship(
        "CompanyUser",
        back_populates="company",
        lazy="select",
        cascade="all, delete-orphan",
    )


class CompanyUser(db.Model, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "company_users"

    company_id = db.Column(db.String(36), db.ForeignKey("companies.id"), nullable=False, index=True)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False, index=True)

    # owner / professional / secretary
    role = db.Column(db.String(50), nullable=False, index=True)

    permissions_json = db.Column(db.JSON, nullable=True)

    is_active = db.Column(db.Boolean, nullable=False, default=True)

    company = db.relationship("Company", back_populates="users", lazy="select")
    user = db.relationship("User", back_populates="company_memberships", lazy="select")

    __table_args__ = (
        db.UniqueConstraint("company_id", "user_id", name="uq_company_users_company_id_user_id"),
    )
