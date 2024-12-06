from flask import (
    Blueprint, render_template, request, redirect, 
    flash, url_for
)
from markupsafe import Markup

from flask_login import login_required, current_user
from .db_manager import fetchall, executeCommit, fetchone
from .models.course import Course
from .models.course_session import CourseSession
import markdown  # Library for rendering Markdown content

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
        courses = fetchall(sql, (user_id,))
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

    # Fetch all pages for the navigation bar
    sql_pages = """
    SELECT ID as page_id, Title as title
    FROM Pages
    WHERE CourseID = %s
    ORDER BY SectionIndex ASC
    """
    sections = fetchall(sql_pages, (course_id,))  # Ensure this returns a list of dictionaries

    if page_id:
        # Fetch specific page details
        sql = "SELECT * FROM Pages WHERE CourseID = %s AND ID = %s"
        page = fetchone(sql, (course_id, page_id))
        if not page:
            flash("Page not found.", "danger")
            return redirect(url_for("views.view_course", course_id=course_id))

        # Render Markdown content
        page["RenderedContent"] = Markup(markdown.markdown(page["Content"]))
        return render_template(
            "view_page.html", 
            course=course, 
            page=page, 
            sections=sections,  # Pass the sections for navigation
            joined=current_user.hasJoinedCourse(course_id)
        )

    # Render about page with sections
    return render_about_page(course, sections)

@blueprint.route("/course/<course_id>/create_page", methods=["GET", "POST"])
@login_required
def create_page(course_id):
    if request.method == "POST":
        # Get form data
        title = request.form.get("title")
        section_index = request.form.get("section_index")
        content = request.form.get("content")

        # Ensure all required fields are provided
        if not title or not section_index or not content:
            flash("All fields are required.", "danger")
            return redirect(url_for("views.create_page", course_id=course_id))

        # Insert into Pages table
        sql = """
        INSERT INTO Pages (CourseID, Title, SectionIndex, Content)
        VALUES (%s, %s, %s, %s)
        """
        try:
            executeCommit(sql, (course_id, title, section_index, content))
            flash("Page created successfully!", "success")
        except Exception as e:
            flash("Failed to create the page.", "danger")
            return redirect(url_for("views.create_page", course_id=course_id))

        return redirect(url_for("views.view_course", course_id=course_id))

    return render_template("create_page.html", course_id=course_id)

# Edit a page
@blueprint.route("/course/<course_id>/<page_id>/edit", methods=["GET", "POST"])
@login_required
def edit_page(course_id, page_id):
    sql_fetch = "SELECT * FROM Pages WHERE ID = %s AND CourseID = %s"
    page = fetchone(sql_fetch, (page_id, course_id))
    if not page:
        flash("Page not found or does not belong to this course.", "danger")
        return redirect(url_for("views.view_course", course_id=course_id))

    if request.method == "POST":
        title = request.form.get("title")
        section_index = request.form.get("section_index")
        content = request.form.get("content")
        sql_update = """
        UPDATE Pages 
        SET Title = %s, SectionIndex = %s, Content = %s, UpdatedAt = CURRENT_TIMESTAMP
        WHERE ID = %s AND CourseID = %s
        """
        executeCommit(sql_update, (title, section_index, content, page_id, course_id))
        flash("Page updated successfully!", "success")
        return redirect(url_for("views.view_course", course_id=course_id, page_id=page_id))
    
    return render_template("edit_page.html", page=page)

# Delete a page
@blueprint.route("/course/<course_id>/<page_id>/delete", methods=["POST"])
@login_required
def delete_page(course_id, page_id):
    sql_delete = "DELETE FROM Pages WHERE ID = %s AND CourseID = %s"
    executeCommit(sql_delete, (page_id, course_id))
    flash("Page deleted successfully!", "success")
    return redirect(url_for("views.view_course", course_id=course_id))

def render_about_page(course, pages):
    participants = course.getParticipants()
    rating = course.getRating() or 0
    sessions = CourseSession.findCourseSessions(course.id)
    return render_template(
        "course_about.html", 
        course=course, 
        pages=pages,
        participants=participants, 
        rating=f"{rating/2}".rstrip('.0'), 
        joined=current_user.hasJoinedCourse(course.id),
        sessions=sessions
    )

@blueprint.route("/course/<course_id>/edit")
def edit_course(course_id=None):
    course = Course.findMatchOR(('ID',), (course_id,))
    if course == None: return "Course does not exist"
    return render_template("edit_course.html", course=course)
