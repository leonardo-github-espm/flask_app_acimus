from flask import Blueprint

bp = Blueprint("webhooks", __name__)

@bp.get("/ping")
def ping():
    return {"ok": True, "module": "webhooks"}
