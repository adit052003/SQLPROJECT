from flask import Blueprint, request, jsonify
from flask_login import current_user
from .models.course import Course
from .db_manager import fetchone, executeCommit

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

@api.route("/api/join_course", methods=['POST'])
def join_course():
    data = request.json
    
    if 'user_id' not in data: return "ERROR: User ID Missing", 400
    if 'course_id' not in data: return "ERROR: Course ID Missing", 400
    
    user_id = data['user_id']
    course_id = data['course_id']
    
    if not fetchone("SELECT ID FROM Users Where ID = %s", (user_id,)):
        return "ERROR: User ID Invalid", 400
    if not fetchone("SELECT ID FROM Courses WHERE ID = %s", (course_id,)):
        return "ERROR: Course ID Invalid", 400
    
    if fetchone("SELECT * FROM JoinedCourses WHERE UserID = %s AND CourseID = %s", (user_id, course_id)):
        return "ERROR: User already joined", 403
    executeCommit("INSERT INTO JoinedCourses (UserID, CourseID) VALUES (%s, %s)", args=(user_id, course_id))
    return "OK"