from ..db_manager import fetchall, fetchone

class Course:
    
    def __init__(self, id, title, code, description, rating=None, registrations=None):
        self.id = id
        self.title = title
        self.description = description
        self.code = code
        self.rating = rating
        self.registrations = registrations
        
    def getParticipants(self):
        sql = '''
        SELECT COUNT(*) FROM JoinedCourses
        WHERE CourseID = %s
        '''
        return fetchone(sql, (self.id,))[0]
    
    def getRating(self):
        sql = '''SELECT AVG(Rating) From CourseRatings WHERE CourseID = %s'''
        return fetchone(sql, (self.id,))[0]
        
    def findMatchOR(keys, values):
        sql = "SELECT `Id`, `Title`, `Code`, `Description` FROM Courses WHERE "
        where = ' OR '.join(map(lambda k: f"`{k}` = %s", keys))
        print(sql + where)
        result = fetchone(sql + where, values)
        if not result: return None
        return Course(*result)

    def fetchAll():
        sql = """
        SELECT `ID`, `Title`, `Code`, `Description` FROM Courses;
        """
        result = fetchall(sql)
        if not result: return None
        return [Course(*row) for row in result]
        
    def fetchAllRatings():
        sql = """
        SELECT C.ID, C.Title, Code, `Description`, Rating, IFNULL(Registrations, 0) FROM Courses C
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
        result = fetchall(sql)
        if not result: return None
        return [Course(*row) for row in result]
    
    def fetchJoinedCourses(user_id):
        sql = """
        SELECT Courses.ID, Courses.Title, Courses.Code, Course.Description, JoinedCourses.JoinDate, JoinedCourses.ViewDate
        FROM JoinedCourses
        JOIN Courses ON JoinedCourses.CourseID = Courses.ID
        WHERE JoinedCourses.UserID = %s
        ORDER BY JoinedCourses.JoinDate DESC
        """
        courses = fetchall(sql, (user_id,))
        return [Course(*c) for c in courses]
    
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'code': self.code,
            'rating': self.rating,
            'registrations': self.registrations
        }