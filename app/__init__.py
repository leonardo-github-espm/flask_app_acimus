from flask import Flask, redirect, url_for
from flask_login import current_user
from .config import Config
from .extensions import db, migrate, login_manager, csrf, limiter, talisman
from .blueprints import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    talisman.init_app(app)

    # Import models so migrations see them
    from . import models  # noqa: F401

    # Blueprints
    register_blueprints(app)

    @app.get("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("agenda.today"))
        return redirect(url_for("auth.login"))

    return app
