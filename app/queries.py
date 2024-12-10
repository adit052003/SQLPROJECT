from .db_manager import fetchall, executeCommit, fetchone
import os
from flask import current_app as app

####  Courses ####

def get_course(course_id):
    sql = "SELECT * FROM Courses WHERE ID=%s"
    return fetchone(sql, course_id)

def get_courses_full_details():
    sql = "SELECT * FROM CoursesFullDetails"
    courses = fetchall(sql)
    for course in courses:
        course['ImageURL'] = f'/files/{course["ImageID"]}' if course["ImageID"] else None
    return courses


def get_rating(course_id):
    sql = '''SELECT AVG(Rating) AS Rating From CourseRatings WHERE CourseID = %s'''
    return fetchone(sql, course_id)['Rating'] or 0

def add_course(course_title, course_code, course_description):
    sql = "INSERT INTO courses (Title, Code, Description) VALUES (%s, %s, %s)"
    executeCommit(sql, (course_title, course_code, course_description))
    return fetchone("SELECT LAST_INSERT_ID() AS ID")['ID'] 
    
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
    sql = """
    SELECT * 
    FROM SessionsFullDetails 
    WHERE CourseID = %s
    """
    sessions = fetchall(sql, (course_id,))
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
    sql = """
    SELECT CourseID AS ID, Title, Code, Description, ImageID, JoinDate, ViewDate
    FROM JoinedCoursesView
    WHERE UserID = %s
    ORDER BY ViewDate DESC
    """
    # Use the view to fetch data
    courses = fetchall(sql, (user_id,))
    for course in courses:
        # Add dynamic ImageURL for each course
        course['ImageURL'] = f'/files/{course["ImageID"]}' if course["ImageID"] else None
    return courses


def update_view_date(course_id, user_id):
    executeCommit("UPDATE JoinedCourses SET ViewDate = now() WHERE CourseID=%s AND UserID=%s", (course_id, user_id))

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
    
# **** Ratings ****

def rate_course(course_id, user_id, rating):
    old_rating = fetchone("SELECT * FROM CourseRatings WHERE UserID=%s AND CourseID=%s", (user_id, course_id))
    if old_rating:
        executeCommit("UPDATE CourseRatings SET Rating=%s WHERE UserID=%s AND CourseID=%s", (rating, user_id, course_id))
    else:
        executeCommit("INSERT INTO CourseRatings (UserID, CourseID, Rating) VALUES (%s, %s, %s)", (user_id, course_id, rating))

def rate_session(session_id, user_id, rating):
    old_rating = fetchone("SELECT * FROM SessionRatings WHERE UserID=%s AND SessionID=%s", (user_id, session_id))
    if old_rating:
        executeCommit("UPDATE SessionRatings SET Rating=%s WHERE UserID=%s AND SessionID=%s", (rating, user_id, session_id))
    else:
        executeCommit("INSERT INTO SessionRatings (UserID, SessionID, Rating) VALUES (%s, %s, %s)", (user_id, session_id, rating))
        
# **** Pages ****

def get_page(course_id, page_id):
    return fetchone("SELECT * FROM Pages WHERE CourseID=%s AND ID=%s", (course_id, page_id))

def get_course_page_titles(course_id):
    return fetchall("SELECT ID, Title FROM Pages WHERE CourseID=%s", course_id)

def get_page_content(page_id):
    return fetchone("SELECT Content FROM Pages WHERE ID=%s", page_id)['Content']

def add_page(course_id, title, content):
    executeCommit("INSERT INTO Pages (CourseID, Title, Content) VALUES (%s, %s, %s)", (course_id, title, content))
    return fetchone("SELECT LAST_INSERT_ID() AS ID")['ID']

def edit_page(page_id, title, content):
    executeCommit("UPDATE Pages SET Title=%s, Content=%s WHERE ID=%s", (title, content, page_id))
    
def delete_page(course_id, page_id):
    executeCommit("DELETE FROM Pages WHERE CourseID=%s AND ID=%s", (course_id, page_id))
    