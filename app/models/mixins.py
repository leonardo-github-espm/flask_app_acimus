# app/models/mixins.py
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from ..extensions import db


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def gen_uuid() -> str:
    return str(uuid.uuid4())


class UUIDPrimaryKeyMixin:
    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)


class TimestampMixin:
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True, onupdate=utcnow)
