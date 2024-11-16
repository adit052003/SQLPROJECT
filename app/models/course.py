from ..db_manager import fetchall, fetchone

class Course:
    
    def __init__(self, id, title, code, rating=None, registrations=None):
        self.id = id
        self.title = title
        self.code = code
        self.rating = rating
        self.registrations = registrations
        
    def findMatchOR(keys, values):
        sql = "SELECT `Id`, `Title`, `Code` FROM Courses WHERE "
        where = ' OR '.join(map(lambda k: f"`{k}` = %s", keys))
        print(sql + where)
        result = fetchone(sql + where, values)
        if not result: return None
        return Course(*result)

    def fetchAll():
        sql = """
        SELECT `ID`, `Title`, `Code` FROM Courses;
        """
        result = fetchall(sql)
        if not result: return None
        return [Course(*row) for row in result]
        
    def fetchAllRatings():
        sql = """
        SELECT C.ID, C.Title, Code, Rating, IFNULL(Registrations, 0) FROM Courses C
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
    
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'code': self.code,
            'rating': self.rating,
            'registrations': self.registrations
        }