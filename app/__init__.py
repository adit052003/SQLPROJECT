from flask import Flask
from flask_login import LoginManager
from app import views, auth
from .db_manager import initialize_db
from .models.user import User

CONFIG_FILE = "../application.cfg"

def create_app():
    app = Flask(__name__)
    app.register_blueprint(views.blueprint)
    app.register_blueprint(auth.auth)
    app.config.from_pyfile(CONFIG_FILE)
    initialize_db(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.findMatchOR(('ID',), (user_id))

    return app