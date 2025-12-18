from flask import Flask

def register_blueprints(app: Flask):
    from .auth.routes import bp as auth_bp
    from .webhooks.routes import bp as webhooks_bp
    from .agenda.routes import bp as agenda_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(webhooks_bp, url_prefix="/webhooks")
    app.register_blueprint(agenda_bp, url_prefix="/agenda")
