from flask import Blueprint, render_template, request, redirect, flash, render_template, url_for
from flask_login import login_required, current_user
from .db_manager import fetchall, executeCommit, fetchone
from .models.course import Course
from .models.course_session import CourseSession

blueprint = Blueprint("views", __name__)

@blueprint.route("/")
def home():
    return render_template("index.html")

@blueprint.route("/dashboard")
@login_required
def dashboard():
     # SQL query to fetch the courses the user has joined
    sql = """
    SELECT Courses.ID, Courses.Title, Courses.Code, JoinedCourses.JoinDate, JoinedCourses.ViewDate
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

@blueprint.route("/course/<course_id>")
@blueprint.route("/course/<course_id>/<page_id>")
@login_required
def view_course(course_id=None, page_id=None):
    course = Course.findMatchOR(('ID',), (course_id,))
    if course == None: return "Course does not exist"
    if page_id == None: return render_about_page(course)
    return render_template("view_course.html", course=course, page_id=page_id, joined=current_user.hasJoinedCourse(course_id))

def render_about_page(course):
    participants = course.getParticipants()
    rating = course.getRating() or 0
    sessions = CourseSession.findCourseSessions(course.id)
    return render_template(
        "course_about.html", 
        course=course, 
        participants=participants, 
        rating=f"{rating/2}".rstrip('.0'), 
        joined=current_user.hasJoinedCourse(course.id),
        sessions = sessions
    )

@blueprint.route("/course/<course_id>/edit")
def edit_course(course_id=None):
    course = Course.findMatchOR(('ID',), (course_id,))
    if course == None: return "Course does not exist"
    return render_template("edit_course.html", course=course)