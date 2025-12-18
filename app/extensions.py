from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

limiter = Limiter(key_func=get_remote_address)


talisman = Talisman(
    force_https=False,
    content_security_policy=None
)

@login_manager.user_loader
def load_user(user_id):
    from .models.user import User
    return User.query.get(user_id)