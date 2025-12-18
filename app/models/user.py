# app/models/user.py
from __future__ import annotations

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from ..extensions import db
from .mixins import UUIDPrimaryKeyMixin, TimestampMixin


class User(db.Model, UserMixin, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "users"

    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    full_name = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    last_login_at = db.Column(db.DateTime(timezone=True), nullable=True)

    # relacionamento reverso: company memberships
    company_memberships = db.relationship(
        "CompanyUser",
        back_populates="user",
        lazy="select",
        cascade="all, delete-orphan",
    )

    def set_password(self, raw_password: str) -> None:
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)
