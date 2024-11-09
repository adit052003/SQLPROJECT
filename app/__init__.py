from flask import Flask
from app import views, auth
from .db_manager import initialize_db

CONFIG_FILE = "../application.cfg"

def create_app():
    app = Flask(__name__)
    app.register_blueprint(views.blueprint)
    app.register_blueprint(auth.auth)
    app.config.from_pyfile(CONFIG_FILE)
    initialize_db(app)
    return app