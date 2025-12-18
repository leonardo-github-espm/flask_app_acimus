# app/models/api.py
from __future__ import annotations

import secrets
import hashlib
from datetime import datetime, timezone

from ..extensions import db
from .mixins import UUIDPrimaryKeyMixin, TimestampMixin


class ApiKey(db.Model, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "api_keys"

    company_id = db.Column(db.String(36), db.ForeignKey("companies.id"), nullable=False, index=True)

    name = db.Column(db.String(255), nullable=False)

    token_prefix = db.Column(db.String(20), nullable=False, index=True)
    token_hash = db.Column(db.String(64), nullable=False, unique=True, index=True)

    scopes_json = db.Column(db.JSON, nullable=True)

    is_active = db.Column(db.Boolean, nullable=False, default=True)

    expires_at = db.Column(db.DateTime(timezone=True), nullable=True)
    last_used_at = db.Column(db.DateTime(timezone=True), nullable=True)

    created_by_user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=True, index=True)

    @staticmethod
    def generate_token(prefix: str = "acm_live") -> str:
        return f"{prefix}_{secrets.token_urlsafe(32)}"

    @staticmethod
    def hash_token(raw_token: str) -> str:
        return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()

    @classmethod
    def create_new(
        cls,
        *,
        company_id: str,
        name: str,
        scopes: list[str] | None,
        created_by_user_id: str | None = None,
        prefix: str = "acm_live",
    ) -> tuple["ApiKey", str]:
        raw = cls.generate_token(prefix=prefix)
        token_hash = cls.hash_token(raw)

        api_key = cls(
            company_id=company_id,
            name=name,
            token_prefix=raw[:20],
            token_hash=token_hash,
            scopes_json=scopes or [],
            is_active=True,
            created_by_user_id=created_by_user_id,
        )
        return api_key, raw
