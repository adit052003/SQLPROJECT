from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .db_manager import fetchall, executeCommit, fetchone
from flask import flash, render_template, redirect, url_for

blueprint = Blueprint("views", __name__)

@blueprint.route("/")
def home():
    return render_template("index.html")

@blueprint.route("/dashboard")
@login_required
def dashboard():
     # SQL query to fetch the courses the user has joined
    sql = """
    SELECT Courses.Title, Courses.Code, JoinedCourses.JoinDate, JoinedCourses.ViewDate
    FROM JoinedCourses
    JOIN Courses ON JoinedCourses.CourseID = Courses.ID
    WHERE JoinedCourses.UserID = %s
    ORDER BY JoinedCourses.JoinDate DESC
    """
    
    try:
        # Fetch the list of joined courses for the current user
        user_id = current_user.id
        courses = fetchall(sql, (user_id,))
    except Exception as e:
        flash("An error occurred while fetching your courses.", "danger")
        courses = []

    # Render the dashboard template with the user's name and courses
    return render_template("dashboard.html", name=current_user.first_name, courses=courses)
    
@blueprint.route("/courses")
@login_required
def courses():
    return render_template("courses.html")