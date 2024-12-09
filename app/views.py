from flask import (
    Blueprint, render_template, request, redirect, 
    flash, url_for
)
from flask_login import login_required, current_user
from . import queries

blueprint = Blueprint("views", __name__)

@blueprint.route("/")
def home():
    return render_template("index.html")

@blueprint.route("/dashboard")
@login_required
def dashboard():
    courses = queries.get_joined_courses(current_user.id)
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
def view_course(course_id=None, page_id=None):
    course = queries.get_course(course_id)
    if course == None: return "Course does not exist"
    
    if queries.has_joined_course(course_id, current_user.id):
        queries.update_view_date(course_id, current_user.id)
    
    sections = queries.get_course_sections(course_id)
    if page_id == None: return render_about_page(course, sections)
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
    participants = queries.get_participant_count(course['ID'])
    rating = queries.get_rating(course['ID'])
    sessions = queries.get_course_sessions_full_details(course['ID'])
    return render_template(
        "course_about.html", 
        course=course, 
        sections=sections,
        participants=participants, 
        rating=f"{rating/2}".rstrip('.0'), 
        joined=current_user.hasJoinedCourse(course['ID']),
        sessions = sessions
    )

@blueprint.route("/course/<course_id>/edit")
def edit_course(course_id=None):
    course = queries.get_course(course_id)
    if course == None: return "Course does not exist"
    course['ImageURL'] = f'/files/{course["ImageID"]}' if course['ImageID'] else None
    return render_template("edit_course.html", course=course)
