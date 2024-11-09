from flask import Blueprint, render_template

blueprint = Blueprint("views", __name__)

@blueprint.route("/")
def home():
    return render_template("index.html")

@blueprint.route("/dashboard")
def dasboard():
    return render_template("dashboard.html")