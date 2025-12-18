# app/models/billing.py
from __future__ import annotations

from ..extensions import db
from .mixins import UUIDPrimaryKeyMixin, TimestampMixin


class Plan(db.Model, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "plans"

    # starter / basic / advanced / premium
    name = db.Column(db.String(50), nullable=False, unique=True, index=True)

    # Ex: {"max_users": 3, "ai_enabled": false, ...}
    features_json = db.Column(db.JSON, nullable=True)

    is_active = db.Column(db.Boolean, nullable=False, default=True)

    subscriptions = db.relationship("Subscription", back_populates="plan", lazy="select")


class Subscription(db.Model, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "subscriptions"

    group_id = db.Column(db.String(36), db.ForeignKey("groups.id"), nullable=False, index=True)
    plan_id = db.Column(db.String(36), db.ForeignKey("plans.id"), nullable=False, index=True)

    # active / trial / canceled / past_due
    status = db.Column(db.String(50), nullable=False, default="trial", index=True)

    started_at = db.Column(db.DateTime(timezone=True), nullable=True)
    ends_at = db.Column(db.DateTime(timezone=True), nullable=True)

    # Provider info (Stripe/Pagar.me/etc.)
    provider = db.Column(db.String(50), nullable=True)
    provider_customer_id = db.Column(db.String(255), nullable=True)
    provider_subscription_id = db.Column(db.String(255), nullable=True)

    plan = db.relationship("Plan", back_populates="subscriptions", lazy="select")

    __table_args__ = (
        db.Index("ix_subscriptions_group_status", "group_id", "status"),
    )
