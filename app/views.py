from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models.course import Course

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

@blueprint.route("/course/<id>")
@login_required
def view_course(id=None):
    course = Course.findMatchOR(('ID',), (id,))
    if course == None: return "Course does not exist"
    return render_template("view_course.html", course=course)