from ..db_manager import fetchall, fetchone

class CourseSession:
    
    def __init__(self, id, course_id, pfn, pln, start_date, end_date, classroom, time, title, description, rating):
        self.id = id
        self.course_id = course_id
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
        
    def findCourseSessions(courseID):
        sql = '''
        SELECT 
        S.`ID`, `CourseID`, `FirstName`, `LastName`, `StartDate`, `EndDate`, `Classroom`, `Time`, `Title`, `Description`, AVG(R.Rating)
        FROM Sessions S
        JOIN Professors P ON S.ProfessorID = P.ID
        JOIN SessionRatings R ON S.ID = R.SessionID
        WHERE CourseID = %s
        GROUP BY S.ID
        '''
        result = fetchall(sql, (courseID,))
        if not result: return None
        return [CourseSession(*row) for row in result]