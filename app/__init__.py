from flask import Flask
from app import views

def create_app():
    app = Flask(__name__)
    app.register_blueprint(views.blueprint)
    return app