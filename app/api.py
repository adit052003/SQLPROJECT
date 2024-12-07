from flask import Blueprint, request, send_from_directory
from flask import current_app as app
from flask_login import current_user
from .db_manager import fetchone
from datetime import datetime
from . import queries

api = Blueprint("api", __name__)

# **** Courses **** 

@api.route("/api/course_list", methods=['POST'])
def course_list():
    courses = queries.get_courses_full_details()
    return courses

@api.route("/api/edit_course", methods=['POST'])
def edit_course():
    data = request.json
    
    if 'course_id' not in data: return { 'reason': "ERROR: Course ID Missing" }, 400
    course = queries.get_course(data['course_id'])
    if not course: return { 'reason': "ERROR: Course ID Invalid" }, 400
    if not queries.has_joined_course(course['ID'], current_user.id): return "ERROR: User has not joined course", 403
    
    title = data.get('title', course['Title'])
    code = data.get('title', course['Code'])
    description = data.get('title', course['Description'])

    queries.edit_course(course['ID'], title, code, description)    
    return {}

@api.route("/api/get_sections", methods=['POST'])
def get_sections():
    data = request.json
    if 'course_id' not in data: return { 'reason': "ERROR: Course ID Missing" }, 400
    return queries.get_course_sections(data['course_id'])


# **** Sessions ****

@api.route("/api/get_sessions", methods=['POST'])
def get_sessions():
    data = request.json
    if 'course_id' not in data: return { 'reason': "ERROR: Course ID Missing" }, 400
    return queries.get_course_sessions(data['course_id'])


@api.route("/api/add_session", methods=['POST'])
def add_session():
    data = request.json
    if 'course_id' not in data: return { 'reason': "ERROR: Course ID Missing" }, 400
    course = queries.get_course(data['course_id'])
    if not course: return { 'reason': "ERROR: Course ID Invalid" }, 400
    if not queries.has_joined_course(course['ID'], current_user.id): return "ERROR: User has not joined course", 403
    
    if 'title' not in data: return { 'reason': "Session Title Missing" }, 403
    if 'professor_id' not in data: return { 'reason': "Professor ID Missing" }, 403
    if 'start_date' not in data: return { 'reason': "Start Date Missing" }, 403
    if 'end_date' not in data: return { 'reason': "End Date Missing" }, 403
    
    title = data['title']
    professor_id = data['professor_id']
    start_date = data['start_date']
    end_date = data['end_date']
    classroom = data.get('classroom', None)
    time = data.get('time', None)
    description = data.get('description', None)
    
    if not queries.get_professor(professor_id): return { 'reason': "Professor ID Invalid" }, 403
    
    if type(start_date) == str: start_date = datetime.fromisoformat(start_date).date()
    if type(end_date) == str: end_date = datetime.fromisoformat(end_date).date()
    
    queries.add_session(course['ID'], title, professor_id, start_date, end_date, classroom, time, description)
    return {}
    
@api.route("/api/edit_session", methods=['POST'])
def edit_session():
    data = request.json
    if 'session_id' not in data: return { 'reason': "ERROR: Session ID Missing" }, 400
    session = queries.get_session(data['session_id'])
    if not session: return { 'reason': "Session ID Invalid" }, 400
    if not queries.has_joined_course(session['CourseID'], current_user.id): return { 'reason': "User has not joined course" }, 403
    
    title = data.get('title', session['Title'])
    professor_id = data.get('professor_id', session['ProfessorID'])
    start_date = data.get('start_date', session['StartDate'])
    end_date = data.get('end_date', session['EndDate'])
    classroom = data.get('classroom', session['Classroom'])
    time = data.get('time', session['Time'])
    description = data.get('description', session['Description'])
    
    if not queries.get_professor(professor_id): return { 'reason': "Professor ID Invalid" }, 403
    
    if type(start_date) == str: start_date = datetime.fromisoformat(start_date).date()
    if type(end_date) == str: end_date = datetime.fromisoformat(end_date).date()

    queries.edit_session(session['ID'], title, professor_id, start_date, end_date, classroom, time, description)    
    return {}
  
@api.route("/api/delete_session", methods=['POST'])
def delete_session():
    data = request.json
    
    if 'session_id' not in data: return { 'reason': "ERROR: Session ID Missing" }, 400
    session = queries.get_session(data['session_id'])
    if not session: return { 'reason': "Session ID Invalid" }, 400
    
    if queries.has_joined_course(session['CourseID'], current_user.id): return { 'reason': "User has not joined course" }, 403
    queries.delete_session(session['ID'])
    return {}


# **** Professors ****

@api.route("/api/get_professors", methods=['POST'])
def get_professors():
    return queries.get_all_professors()

@api.route("/api/add_professor", methods=['POST'])
def add_professor():
    data = request.json
    if 'first_name' not in data: return { 'reason': "First Name Missing"}, 400
    if 'last_name' not in data: return { 'reason': "Last Name Missing"}, 400
    professor_id = queries.add_professor(data['first_name'], data['last_name'])
    return {'new_id': professor_id}

# **** Joined Courses ****

@api.route("/api/joined_courses", methods=['GET'])
def joined_courses():
    user_id = current_user.id
    return queries.get_joined_courses(user_id)

@api.route("/api/join_course", methods=['POST'])
def join_course():
    data = request.json
    
    if 'course_id' not in data: return { 'reason': "ERROR: Course ID Missing" }, 400
    course_id = data['course_id']
    
    if not queries.get_course(course_id): return { 'reason': "ERROR: Course ID Invalid" }, 400
    if queries.has_joined_course(course_id, current_user.id): return { 'reason': "ERROR: User Already Joined Course" }, 403
    queries.join_course(course_id, current_user.id)
    return {}

# **** Course Sections ****

@api.route("/api/add_section", methods=['POST'])
def add_section():
    data = request.json
    
    if 'course_id' not in data: return { 'reason': "ERROR: Course ID Missing" }, 400
    if not queries.get_course(data['course_id']): return { 'reason': "ERROR: Course ID Invalid" }, 400
    if queries.has_joined_course(data['course_id'], current_user.id): return { 'reason': "User has not joined course" }, 403
    
    if 'title' not in data: return { 'reason': "Section Title Missing" }, 403
    if 'page_id' not in data: return { 'reason': "Page ID Missing" }, 403
    
    # TODO: Check PageID Valid
    # if not fetchone("SELECT * FROM Professors WHERE ID = %s", (professor_id,)):
    #     return { 'reason': "Professor ID Invalid" }, 403
    
    queries.add_section(data['course_id'], data['title'], data['page_id'])
    return {}
    
@api.route("/api/edit_section", methods=['POST'])
def edit_section():
    data = request.json
    
    if 'section_id' not in data: return { 'reason': "Session ID Missing" }, 400
    section = queries.get_section(data['section_id'])
    if not section: return { 'reason': "Session ID Invalid" }, 400
    if queries.has_joined_course(section['CourseID'], current_user.id): return { 'reason': "User has not joined course" }, 403
    
    title = data.get('title', section['Title'])
    page_id = data.get('page_id', section['PageID'])
    
    # TODO: Check Page ID Valid
    # if not fetchone("SELECT * FROM Professors WHERE ID = %s", (professor_id,)):
    #     return { 'reason': "Professor ID Invalid" }, 403
    
    queries.edit_section(section['ID'], title, page_id)
    return {}

  
@api.route("/api/delete_section", methods=['POST'])
def delete_section():
    data = request.json
    if 'section_id' not in data: return { 'reason': "Section ID Missing" }, 400
    section = queries.get_section(data['section_id'])
    if not section: return { 'reason': "Session ID Invalid" }, 400
    if queries.has_joined_course(section['CourseID'], current_user.id): return { 'reason': "User has not joined course" }, 403
    queries.delete_section(section['ID'])
    return {}

# **** Files ****

@api.route("/api/upload_course_image", methods=['POST'])
def upload_course_image():
    if 'course_id' not in request.form: return { 'reason': "Course ID Missing" }, 400
    course = queries.get_course(request.form['course_id'])
    if not course: return { 'reason': "Course ID Invalid" }, 400
    
    if len(request.files) > 0:
        file = request.files['file']
        if course['ImageID']: 
            queries.edit_file(course['ImageID'], file)
        else: 
            file_id = queries.add_file(file)
            queries.set_course_image_id(course['ID'], file_id)
    else:
        if course['ImageID']:
            queries.delete_file(course['ImageID'])
            queries.set_course_image_id(course['ID'], None)
    return {}

@api.route("/files/<id>")
def get_file(id):
    return send_from_directory(app.config["UPLOAD_FOLDER"], queries.get_real_filename(id))