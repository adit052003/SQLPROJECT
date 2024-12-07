from .db_manager import fetchall, executeCommit, fetchone
import os
from flask import current_app as app

####  Courses ####

def get_course(course_id):
    sql = "SELECT * FROM Courses WHERE ID=%s"
    return fetchone(sql, course_id)

def get_courses_full_details():
    sql = """
    SELECT C.ID, C.Title, Code, Description, ImageID, Rating, IFNULL(Registrations, 0) AS Registrations FROM Courses C
    LEFT JOIN (
        SELECT CourseID, AVG(Rating) AS Rating
        FROM CourseRatings
        GROUP BY CourseID
    ) R ON R.CourseID = C.ID
    LEFT JOIN (
        SELECT CourseID, COUNT(*) AS Registrations
        FROM JoinedCourses
        GROUP BY CourseID
    ) J ON J.CourseID = C.ID
    """
    courses = fetchall(sql)
    for course in courses: course['ImageURL'] = f'/files/{course["ImageID"]}' if course["ImageID"] else None
    return courses

def get_rating(course_id):
    sql = '''SELECT AVG(Rating) AS Rating From CourseRatings WHERE CourseID = %s'''
    return fetchone(sql, course_id)['Rating'] or 0

def add_course(course_title, course_code, course_description):
    sql = "INSERT INTO courses (Title, Code, Description) VALUES (%s, %s, %s)"
    executeCommit(sql, (course_title, course_code, course_description))
    
def edit_course(course_id, title, code, description):
    executeCommit(
        "UPDATE Courses SET Title=%s, Code=%s, Description=%s WHERE ID=%s", 
        (title, code, description, course_id)
    )

def set_course_image_id(course_id, image_id):
    executeCommit("UPDATE Courses SET ImageID = %s WHERE ID = %s", (image_id, course_id))
    
#### Sessions ####

def get_session(session_id):
    return fetchone("SELECT * FROM Sessions WHERE ID=%s", session_id)

def get_course_sessions(course_id):
    sql = '''
    SELECT * FROM Sessions S
    WHERE CourseID = %s
    '''
    sessions = fetchall(sql, course_id)
    for session in sessions:
        session['StartDate'] = f"{session['StartDate'].year}-{session['StartDate'].month:02}-{session['StartDate'].day:02}"
        session['EndDate'] = f"{session['EndDate'].year}-{session['EndDate'].month:02}-{session['EndDate'].day:02}"
    return sessions
    
def get_course_sessions_full_details(course_id):
    sql = '''
    SELECT 
    S.ID, CourseID, StartDate, EndDate, Classroom, Time, Title, Description, 
    FirstName, LastName, AVG(R.Rating) AS Rating
    FROM Sessions S
    JOIN Professors P ON S.ProfessorID = P.ID
    JOIN SessionRatings R ON S.ID = R.SessionID
    WHERE CourseID = %s
    GROUP BY S.ID
    '''
    sessions = fetchall(sql, course_id)
    for session in sessions:
        session['StartDate'] = f"{session['StartDate'].year}-{session['StartDate'].month:02}-{session['StartDate'].day:02}"
        session['EndDate'] = f"{session['EndDate'].year}-{session['EndDate'].month:02}-{session['EndDate'].day:02}"
    return sessions

def add_session(course_id, title, professor_id, start_date, end_date, classroom, time, description):
    executeCommit(
        """
        INSERT INTO Sessions (CourseID, Title, ProfessorID, StartDate, EndDate, Classroom, Time, Description) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, 
        (course_id, title, professor_id, start_date, end_date, classroom, time, description)
    )
    
def edit_session(session_id, title, professor_id, start_date, end_date, classroom, time, description):
    executeCommit(
        "UPDATE Sessions SET Title=%s, ProfessorID=%s, StartDate=%s, EndDate=%s, Classroom=%s, Time=%s, Description=%s WHERE ID=%s", 
        (title, professor_id, start_date, end_date, classroom, time, description, session_id)
    )
    
def delete_session(session_id):
    executeCommit("DELETE FROM Sessions WHERE ID=%s", session_id)

#### Professors ####

def get_all_professors():
    sql = "SELECT * FROM Professors"
    return fetchall(sql)

def get_professor(professor_id):
    sql = "SELECT * FROM Professors WHERE ID = %s"
    return fetchall(sql, professor_id)

def add_professor(first_name, last_name):
    executeCommit("INSERT INTO Professors (FirstName, LastName) VALUES (%s, %s)", args=(first_name, last_name))
    return fetchone("SELECT LAST_INSERT_ID() AS ID")['ID']

#### Joined Courses ####

def has_joined_course(course_id, user_id):
    return bool(fetchone("SELECT * FROM JoinedCourses WHERE UserID = %s AND CourseID = %s", (user_id, course_id)))

def join_course(course_id, user_id):
    executeCommit("INSERT INTO JoinedCourses (UserID, CourseID) VALUES (%s, %s)", args=(user_id, course_id))
    
def get_participant_count(course_id):
    sql = '''
    SELECT COUNT(*) AS pcount FROM JoinedCourses
    WHERE CourseID = %s
    '''
    return fetchone(sql, course_id)['pcount']

def get_joined_courses(user_id):
     # SQL query to fetch the courses the user has joined
    sql = """
    SELECT Courses.ID, Courses.Title, Courses.Code, JoinedCourses.JoinDate, JoinedCourses.ViewDate
    FROM JoinedCourses
    JOIN Courses ON JoinedCourses.CourseID = Courses.ID
    WHERE JoinedCourses.UserID = %s
    ORDER BY JoinedCourses.JoinDate DESC
    """
    return fetchall(sql, user_id)

# **** Course Sections ****

def get_section(section_id):
    return fetchone("SELECT * FROM CourseSections WHERE ID=%s", section_id)

def get_course_sections(course_id):
    sql = '''
    SELECT * FROM CourseSections
    WHERE CourseID = %s
    '''
    return fetchall(sql, course_id)

def add_section(course_id, title, page_id):
    executeCommit(
        "INSERT INTO CourseSections (CourseID, Title, PageID) VALUES (%s, %s, %s)", 
        (course_id, title, page_id))

def edit_section(section_id, title, page_id):
    executeCommit("UPDATE CourseSections SET Title=%s, PageID=%s WHERE ID=%s", (title, page_id, section_id))
    
def delete_section(section_id):
    executeCommit("DELETE FROM CourseSections WHERE ID=%s", section_id)
    

# **** Files ****

def get_real_filename(id):
    file = fetchone("SELECT Filename FROM Files Where ID=%s", id)['Filename']
    extension = file.split('.')[-1]
    return f'{id}.{extension}'

def add_file(file):
    executeCommit("INSERT INTO Files (Filename) VALUES (%s)", file.filename)
    file_id = fetchone("SELECT LAST_INSERT_ID() AS ID")['ID']
    extension = file.filename.split('.')[-1]
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], f'{file_id}.{extension}'))
    return file_id
    
def edit_file(id, file):
    executeCommit("UPDATE Files SET Filename=%s WHERE ID=%s", (file.filename, id))
    extension = file.filename.split('.')[-1]
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], f'{id}.{extension}'))
    
def delete_file(id):
    filename = fetchone("SELECT Filename FROM Files Where ID=%s", id)['Filename']
    executeCommit("DELETE FROM Files WHERE ID=%s", id)
    extension = filename.split('.')[-1]
    os.remove(os.path.join(app.config["UPLOAD_FOLDER"], f'{id}.{extension}'))
    
    