from flask import Blueprint, render_template, request, redirect, flash, render_template, url_for
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
    
    sections = queries.get_course_sections(course_id)
    if page_id == None: return render_about_page(course, sections)
    return render_template("view_course.html", course=course, sections=sections, page_id=page_id, joined=current_user.hasJoinedCourse(course_id))

def render_about_page(course, sections):
    participants = queries.get_participant_count(course['ID'])
    rating = queries.get_rating(course['ID'])
    sessions = queries.get_course_sessions_full_details(course['ID'])
    return render_template(
        "course_about.html", 
        course=course, 
        sections = sections,
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
