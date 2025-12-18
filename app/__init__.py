from flask import Flask
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

    # Blueprints
    register_blueprints(app)

    return app
