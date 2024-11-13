from flask import Blueprint, render_template
from flask_login import login_required, current_user

blueprint = Blueprint("views", __name__)

@blueprint.route("/")
def home():
    return render_template("index.html")

@blueprint.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", name=current_user.first_name)

@blueprint.route("/courses")
@login_required
def courses():
    return render_template("courses.html")