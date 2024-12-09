from flask import (
    Blueprint, render_template, request, redirect, 
    flash, url_for
)
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
    sql = """
    SELECT Courses.ID, Courses.Title, Courses.Code, 
           JoinedCourses.JoinDate, JoinedCourses.ViewDate
    FROM JoinedCourses
    JOIN Courses ON JoinedCourses.CourseID = Courses.ID
    WHERE JoinedCourses.UserID = %s
    ORDER BY JoinedCourses.JoinDate DESC
    """
    try:
        user_id = current_user.id
        courses = fetchall(sql, (user_id,), as_dict=False)
    except Exception as e:
        flash("An error occurred while fetching your courses.", "danger")
        courses = []

    return render_template("dashboard.html", name=current_user.first_name, courses=courses)

@blueprint.route("/courses")
@login_required
def courses():
    return render_template("courses.html")

# Create a course
@blueprint.route("/create_course", methods=['GET', 'POST'])
@login_required
def create_course():
    if request.method == 'POST':
        course_title = request.form['Title']
        course_code = request.form['Code']
        course_description = request.form['Description']
        sql = "INSERT INTO courses (Title, Code, Description) VALUES (%s, %s, %s)"
        executeCommit(sql, (course_title, course_code, course_description))
        flash("Course created successfully!", "success")
        return redirect(url_for("views.dashboard"))
    return render_template("add_course.html")

@blueprint.route("/course/<course_id>")
@blueprint.route("/course/<course_id>/<page_id>")
@login_required
def view_course(course_id, page_id=None):
    # Fetch course details
    course = Course.findMatchOR(('ID',), (course_id,))
    if not course:
        flash("Course does not exist.", "danger")
        return redirect(url_for("views.dashboard"))
    
    sql_pages = """
    SELECT ID as page_id, Title as title
    FROM Pages
    WHERE CourseID = %s
    ORDER BY SectionIndex ASC
    """
    sections = fetchall(sql_pages, (course_id,))

    if page_id:
        # Fetch specific page details
        sql = "SELECT ID, Title, Content FROM Pages WHERE CourseID = %s AND ID = %s"
        page_data = fetchone(sql, (course_id, page_id))
        if not page_data:
            flash("Page not found.", "danger")
            return redirect(url_for("views.view_course", course_id=course_id))
        
        # Map SQL data to dictionary
        page = {"ID": page_data[0], "Title": page_data[1], "Content": page_data[2]}
        return render_template(
            "view_page.html",
            course=course,
            page=page,
            sections=sections,
            joined=current_user.hasJoinedCourse(course_id),
        )

    # Render about page if no specific page is requested
    print("Sections passed to template:", sections)

    return render_about_page(course, sections)

@blueprint.route("/course/<course_id>/create_page", methods=["GET", "POST"])
@login_required
def create_page(course_id):
    if request.method == "POST":
        title = request.form.get("title")
        section_index = request.form.get("section_index")
        content = request.form.get("content")

        if not title or not section_index or not content:
            flash("All fields are required.", "danger")
            return redirect(url_for("views.create_page", course_id=course_id))

        sql = """
        INSERT INTO Pages (CourseID, Title, SectionIndex, Content)
        VALUES (%s, %s, %s, %s)
        """
        executeCommit(sql, (course_id, title, section_index, content))
        flash("Page created successfully!", "success")

        return redirect(url_for("views.view_course", course_id=course_id))
    
    return render_template("create_page.html", course_id=course_id)

@blueprint.route("/course/<course_id>/<page_id>/edit", methods=["GET", "POST"])
@login_required
def edit_page(course_id, page_id):
    sql_fetch = "SELECT ID, Title, SectionIndex, Content FROM Pages WHERE ID = %s AND CourseID = %s"
    page_data = fetchone(sql_fetch, (page_id, course_id))
    if not page_data:
        flash("Page not found or does not belong to this course.", "danger")
        return redirect(url_for("views.view_course", course_id=course_id))
    
    page = {"ID": page_data[0], "Title": page_data[1], "SectionIndex": page_data[2], "Content": page_data[3]}

    if request.method == "POST":
        title = request.form.get("title")
        section_index = request.form.get("section_index")
        content = request.form.get("content")
        sql_update = """
        UPDATE Pages 
        SET Title = %s, SectionIndex = %s, Content = %s
        WHERE ID = %s AND CourseID = %s
        """
        executeCommit(sql_update, (title, section_index, content, page_id, course_id))
        flash("Page updated successfully!", "success")
        return redirect(url_for("views.view_course", course_id=course_id, page_id=page_id))

    return render_template("edit_page.html", page=page)

@blueprint.route("/course/<course_id>/<page_id>/delete", methods=["POST"])
@login_required
def delete_page(course_id, page_id):
    sql_delete = "DELETE FROM Pages WHERE ID = %s AND CourseID = %s"
    executeCommit(sql_delete, (page_id, course_id))
    flash("Page deleted successfully!", "success")
    return redirect(url_for("views.view_course", course_id=course_id))

def render_about_page(course, sections):
    participants = course.getParticipants()
    rating = course.getRating() or 0
    sessions = CourseSession.findCourseSessionsRatings(course.id)
    return render_template(
        "course_about.html", 
        course=course, 
        sections=sections,
        participants=participants, 
        rating=f"{rating/2}".rstrip('.0'), 
        joined=current_user.hasJoinedCourse(course.id),
        sessions=sessions
    )

@blueprint.route("/course/<course_id>/edit")
@login_required
def edit_course(course_id):
    course = Course.findMatchOR(('ID',), (course_id,))
    if not course:
        flash("Course does not exist.", "danger")
        return redirect(url_for("views.dashboard"))
    return render_template("edit_course.html", course=course)

