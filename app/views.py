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
@blueprint.route("/create_course")
@login_required
def create_course():
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
    return render_course_page(course, sections, page_id)
    
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
    
def render_course_page(course, sections, page_id):
    page = queries.get_page(course['ID'], page_id)
    if not page: return redirect(url_for("views.view_course", course_id=course['ID']))
    
    return render_template(
        "view_page.html",
        course=course,
        page=page,
        sections=sections,
        joined=current_user.hasJoinedCourse(course['ID']),
    )

@blueprint.route("/course/<course_id>/create_page")
@login_required
def create_page(course_id):
    return render_template("create_page.html", course_id=course_id)

@blueprint.route("/course/<course_id>/create_page", methods=['POST'])
@login_required
def create_page_post(course_id):
    title = request.form.get("title")
    content = request.form.get("content")

    if not title or not content:
        flash("All fields are required.", "danger")
        return redirect(url_for("views.create_page", course_id=course_id))

    page_id = queries.add_page(course_id, title, content)
    return redirect(url_for("views.view_course", course_id=course_id, page_id=page_id))

@blueprint.route("/course/<course_id>/<page_id>/edit")
@login_required
def edit_page(course_id, page_id):
    course = queries.get_course(course_id)
    page = queries.get_page(course_id, page_id)
    if not course: return redirect(url_for("views.dashboard"))
    if not page: return redirect(url_for("views.view_course", course_id=course_id))
    if not queries.has_joined_course(course_id, current_user.id): return redirect(url_for("views.view_course", course_id=course_id))
    
    return render_template("edit_page.html", course_id=course_id, page=page)

@blueprint.route("/course/<course_id>/<page_id>/edit", methods=["POST"])
@login_required
def edit_page_post(course_id, page_id):
    title = request.form.get("title")
    content = request.form.get("content")
    if not title or not content: 
        flash("All fields are required.", "danger")
        return redirect(url_for("views.create_page", course_id=course_id))
    queries.edit_page(page_id, title, content)
    return redirect(url_for("views.view_course", course_id=course_id, page_id=page_id))


@blueprint.route("/course/<course_id>/<page_id>/delete", methods=["POST"])
@login_required
def delete_page(course_id, page_id):
    queries.delete_page(course_id, page_id)
    return redirect(url_for("views.view_course", course_id=course_id))

@blueprint.route("/course/<course_id>/edit")
@login_required
def edit_course(course_id=None):
    course = queries.get_course(course_id)
    if course == None: return "Course does not exist"
    course['ImageURL'] = f'/files/{course["ImageID"]}' if course['ImageID'] else None
    return render_template("edit_course.html", course=course)

@blueprint.route("/course/<course_id>/search")
@login_required
def search_course(course_id):
    course = queries.get_course(course_id)
    if course == None: return redirect(url_for('views.dashboard'))
    return render_template("search_course.html", course=course)