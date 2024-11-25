from flask import Blueprint, request, jsonify
from flask_login import current_user
from .models.course import Course

api = Blueprint("api", __name__)

@api.route("/api/course_list", methods=['POST'])
def course_list():
    courses = Course.fetchAllRatings()
    return jsonify(courses=[c.serialize() for c in courses])

@api.route("/api/joined_courses", methods=['GET'])
def joined_courses():
    user_id = current_user.id
    joined_courses = Course.fetchJoinedCourses(user_id)
    print(joined_courses)  # Debug: Check what data is being returned
    return jsonify(courses=[c.serialize() for c in joined_courses])