from flask import Blueprint, render_template
from .db_manager import test_db

blueprint = Blueprint("views", __name__)

@blueprint.route("/")
def home():
    test_db()
    return render_template("index.html")