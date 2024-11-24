from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from app.db_manager import executeCommit

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

@blueprint.route("/create_course", methods=['GET', 'POST'])
@login_required
def create_course():
    if request.method == 'POST':
        print("Form Submitted!")
        course_title = request.form['Title']
        course_code = request.form['Code']
        course_description = request.form['Description']
        print(f"Title: {course_title}, Code: {course_code}, Description: {course_description}")
        sql = "INSERT INTO courses (Title, Code, Description) VALUES (%s, %s, %s)"

        executeCommit(sql, (course_title, course_code, course_description))
        return redirect("/dashboard")
    return render_template("add_course.html")

