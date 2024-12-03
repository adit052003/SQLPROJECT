from flask import Blueprint, request, jsonify
from flask_login import current_user
from .models.course import Course
from .models.professors import Professor
from .models.course_session import CourseSession
from .models.course_section import CourseSection
from .db_manager import fetchone, executeCommit
from datetime import datetime

api = Blueprint("api", __name__)

@api.route("/api/course_list", methods=['POST'])
def course_list():
    courses = Course.fetchAllRatings()
    return jsonify(courses=[c.serialize() for c in courses])

@api.route("/api/get_professors", methods=['POST'])
def get_professors():
    professors = Professor.getAll()
    return jsonify(professors=[p.serialize() for p in professors])

@api.route("/api/get_sessions", methods=['POST'])
def get_sessions():
    data = request.json
    if 'course_id' not in data: return "ERROR: Course ID Missing", 400
    
    sessions = CourseSession.findCourseSessions(data['course_id'])
    return jsonify(sessions=[s.serialize() for s in sessions])

@api.route("/api/get_sections", methods=['POST'])
def get_sections():
    data = request.json
    if 'course_id' not in data: return "ERROR: Course ID Missing", 400
    
    sections = CourseSection.findCourseSections(data['course_id'])
    return jsonify(sections=[s.serialize() for s in sections])

@api.route("/api/add_professor", methods=['POST'])
def add_professor():
    data = request.json
    if 'first_name' not in data: return { 'reason': "First Name Missing"}, 400
    if 'last_name' not in data: return { 'reason': "Last Name Missing"}, 400
    executeCommit("INSERT INTO Professors (FirstName, LastName) VALUES (%s, %s)", args=(data['first_name'], data['last_name']))
    professor_id = fetchone("SELECT LAST_INSERT_ID()")[0]
    return {'new_id': professor_id}

@api.route("/api/joined_courses", methods=['GET'])
def joined_courses():
    user_id = current_user.id
    joined_courses = Course.fetchJoinedCourses(user_id)
    print(joined_courses)  # Debug: Check what data is being returned
    return jsonify(courses=[c.serialize() for c in joined_courses])

@api.route("/api/join_course", methods=['POST'])
def join_course():
    data = request.json
    
    if 'course_id' not in data: return "ERROR: Course ID Missing", 400
    
    course_id = data['course_id']
    
    if not fetchone("SELECT ID FROM Courses WHERE ID = %s", (course_id,)):
        return "ERROR: Course ID Invalid", 400
    
    if fetchone("SELECT * FROM JoinedCourses WHERE UserID = %s AND CourseID = %s", (current_user.id, course_id)):
        return "ERROR: User already joined", 403
    executeCommit("INSERT INTO JoinedCourses (UserID, CourseID) VALUES (%s, %s)", args=(current_user.id, course_id))
    return "OK"

@api.route("/api/edit_course", methods=['POST'])
def edit_course():
    data = request.json
    
    if 'course_id' not in data: return "ERROR: Course ID Missing", 400
    if 'title' not in data: return "ERROR: Title Missing", 400
    if 'code' not in data: return "ERROR: Title Missing", 400
    if 'description' not in data: return "ERROR: Title Missing", 400
    
    course_id = data['course_id']
    if not fetchone("SELECT ID FROM Courses WHERE ID = %s", (course_id,)):
        return "ERROR: Course ID Invalid", 400
    
    if not fetchone("SELECT * FROM JoinedCourses WHERE UserID = %s AND CourseID = %s", (current_user.id, course_id)):
        return "ERROR: User has not joined course", 403
    
    executeCommit("UPDATE Courses SET Title=%s, Code=%s, Description=%s WHERE ID=%s", args=(data['title'], data['code'], data['description'], course_id))
    return "OK"

@api.route("/api/add_session", methods=['POST'])
def add_session():
    data = request.json
    
    if 'course_id' not in data: return "ERROR: Course ID Missing", 400
    
    course = Course.findMatchOR(('ID',), (data['course_id']))
    if not course:
        return { 'reason': "Course ID Invalid" }, 400
    
    if not fetchone("SELECT * FROM JoinedCourses WHERE UserID = %s AND CourseID = %s", (current_user.id, course.id)):
        return { 'reason': "User has not joined course" }, 403
    
    if 'title' not in data: return { 'reason': "Session Title Missing" }, 403
    if 'professor_id' not in data: return { 'reason': "Professor ID Missing" }, 403
    if 'start_date' not in data: return { 'reason': "Start Date Missing" }, 403
    if 'end_date' not in data: return { 'reason': "End Date Missing" }, 403
    
    title = data['title']
    professor_id = data['professor_id']
    start_date = data['start_date']
    end_date = data['end_date']
    
    if not fetchone("SELECT * FROM Professors WHERE ID = %s", (professor_id,)):
        return { 'reason': "Professor ID Invalid" }, 403
    
    classroom = data.get('classroom', None)
    time = data.get('time', None)
    description = data.get('description', None)
    
    if type(start_date) == str: start_date = datetime.fromisoformat(start_date).date()
    if type(end_date) == str: end_date = datetime.fromisoformat(end_date).date()
    
    executeCommit("INSERT INTO Sessions (CourseID, Title, ProfessorID, StartDate, EndDate, Classroom, Time, Description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", args=(course.id, title, professor_id, start_date, end_date, classroom, time, description))
    return {}
    
@api.route("/api/edit_session", methods=['POST'])
def edit_session():
    data = request.json
    
    if 'session_id' not in data: return "ERROR: Session ID Missing", 400
    
    session_id = data.get('session_id')
    print(data)
    session = CourseSession.findByID(session_id)
    if not session:
        return { 'reason': "Session ID Invalid" }, 400
    
    if not fetchone("SELECT * FROM JoinedCourses WHERE UserID = %s AND CourseID = %s", (current_user.id, session.course_id)):
        return { 'reason': "User has not joined course" }, 403
    
    title = data.get('title', session.title)
    professor_id = data.get('professor_id', session.professor_id)
    start_date = data.get('start_date', session.start_date)
    end_date = data.get('end_date', session.end_date)
    classroom = data.get('classroom', session.classroom)
    time = data.get('time', session.time)
    description = data.get('description', session.description)
    
    if not fetchone("SELECT * FROM Professors WHERE ID = %s", (professor_id,)):
        return { 'reason': "Professor ID Invalid" }, 403
    
    if type(start_date) == str: start_date = datetime.fromisoformat(start_date).date()
    if type(end_date) == str: end_date = datetime.fromisoformat(end_date).date()
    
    executeCommit("UPDATE Sessions SET Title=%s, ProfessorID=%s, StartDate=%s, EndDate=%s, Classroom=%s, Time=%s, Description=%s WHERE ID=%s", args=(title, professor_id, start_date, end_date, classroom, time, description, session_id))
    return {}

  
@api.route("/api/delete_session", methods=['POST'])
def delete_session():
    data = request.json
    
    if 'session_id' not in data: return "ERROR: Session ID Missing", 400
    
    session_id = data.get('session_id')
    session = CourseSession.findByID(session_id)
    if not session:
        return { 'reason': "Session ID Invalid" }, 400
    
    if not fetchone("SELECT * FROM JoinedCourses WHERE UserID = %s AND CourseID = %s", (current_user.id, session.course_id)):
        return { 'reason': "User has not joined course" }, 403
    
    executeCommit("DELETE FROM Sessions WHERE ID=%s", args=(session_id,))
    return {}

@api.route("/api/add_section", methods=['POST'])
def add_section():
    data = request.json
    
    if 'course_id' not in data: return { 'reason': "Course ID Invalid" }, 400

    course = Course.findMatchOR(('ID',), (data['course_id']))
    if not course: return { 'reason': "Course ID Invalid" }, 400
    
    if not fetchone("SELECT * FROM JoinedCourses WHERE UserID = %s AND CourseID = %s", (current_user.id, course.id)):
        return { 'reason': "User has not joined course" }, 403
    
    if 'title' not in data: return { 'reason': "Section Title Missing" }, 403
    if 'page_id' not in data: return { 'reason': "Page ID Missing" }, 403
    
    title = data['title']
    page_id = data['page_id']
    
    # TODO: Check PageID Valid
    # if not fetchone("SELECT * FROM Professors WHERE ID = %s", (professor_id,)):
    #     return { 'reason': "Professor ID Invalid" }, 403
    
    executeCommit("INSERT INTO CourseSections (CourseID, Title, PageID) VALUES (%s, %s, %s)", args=(course.id, title, page_id))
    return {}
    
@api.route("/api/edit_section", methods=['POST'])
def edit_section():
    data = request.json
    
    if 'section_id' not in data: return { 'reason': "Session ID Missing" }, 400
    
    section_id = data.get('section_id')
    print("SectionID", section_id)
    section = CourseSection.findByID(section_id)
    if not section: return { 'reason': "Session ID Invalid" }, 400
    
    if not fetchone("SELECT * FROM JoinedCourses WHERE UserID = %s AND CourseID = %s", (current_user.id, section.course_id)):
        return { 'reason': "User has not joined course" }, 403
    
    title = data.get('title', section.title)
    page_id = data.get('page_id', section.page_id)
    
    # TODO: Check Page ID Valid
    # if not fetchone("SELECT * FROM Professors WHERE ID = %s", (professor_id,)):
    #     return { 'reason': "Professor ID Invalid" }, 403
    
    executeCommit("UPDATE CourseSections SET Title=%s, PageID=%s WHERE ID=%s", args=(title, page_id, section_id))
    return {}

  
@api.route("/api/delete_section", methods=['POST'])
def delete_section():
    data = request.json
    
    if 'section_id' not in data: return { 'reason': "Section ID Missing" }, 400
    
    section_id = data.get('section_id')
    section = CourseSection.findByID(section_id)
    if not section: return { 'reason': "Section ID Invalid" }, 400
    
    if not fetchone("SELECT * FROM JoinedCourses WHERE UserID = %s AND CourseID = %s", (current_user.id, section.course_id)):
        return { 'reason': "User has not joined course" }, 403
    
    executeCommit("DELETE FROM CourseSections WHERE ID=%s", args=(section_id,))
    return {}