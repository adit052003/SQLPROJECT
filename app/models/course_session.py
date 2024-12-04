from ..db_manager import fetchall, fetchone

class CourseSession:
    
    def __init__(self, id, course_id, pid, start_date, end_date, classroom, time, title, description, pfn=None, pln=None, rating=None):
        self.id = id
        self.course_id = course_id
        self.professor_id = pid
        self.professor_first_name = pfn
        self.professor_last_name = pln
        self.start_date = start_date
        self.end_date = end_date
        self.classroom = classroom
        self.time = time
        self.title = title
        self.description = description
        self.rating = rating
        
    def getParticipants(self):
        sql = '''
        SELECT COUNT(*) FROM JoinedCourses
        WHERE CourseID = %s
        '''
        return fetchone(sql, (self.id,))[0]
    
    def getRating(self):
        sql = '''SELECT AVG(Rating) From CourseRatings WHERE CourseID = %s'''
        return fetchone(sql, (self.id,))[0]
    
    def serialize(self):
        return {
            "id": self.id,
            "course_id": self.course_id,
            "professor_id": self.professor_id,
            "start_date": f'{self.start_date.year}-{self.start_date.month:02}-{self.start_date.day:02}',
            "end_date": f'{self.end_date.year}-{self.end_date.month:02}-{self.end_date.day:02}',
            "classroom": self.classroom,
            "time": self.time,
            "title": self.title,
            "description": self.description
        }
        
    def findByID(id):
        sql = '''
        SELECT 
        S.`ID`, `CourseID`, `ProfessorID`, `StartDate`, `EndDate`, `Classroom`, `Time`, `Title`, `Description`
        FROM Sessions S
        WHERE ID = %s
        '''
        result = fetchone(sql, (id,))
        if not result: return None
        return CourseSession(*result)
    
    def findCourseSessions(courseID):
        sql = '''
        SELECT 
        S.`ID`, `CourseID`, `ProfessorID`, `StartDate`, `EndDate`, `Classroom`, `Time`, `Title`, `Description`
        FROM Sessions S
        WHERE CourseID = %s
        '''
        result = fetchall(sql, (courseID,))
        if not result: return None
        return [CourseSession(*row) for row in result]
        
    def findCourseSessionsRatings(courseID):
        sql = '''
        SELECT 
        S.`ID`, `CourseID`, P.ID, `StartDate`, `EndDate`, `Classroom`, `Time`, `Title`, `Description`, `FirstName`, `LastName`, AVG(R.Rating)
        FROM Sessions S
        JOIN Professors P ON S.ProfessorID = P.ID
        JOIN SessionRatings R ON S.ID = R.SessionID
        WHERE CourseID = %s
        GROUP BY S.ID
        '''
        result = fetchall(sql, (courseID,))
        if not result: return None
        return [CourseSession(*row) for row in result]