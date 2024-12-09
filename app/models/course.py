from ..db_manager import fetchall, fetchone
from flask import url_for

class Course:
    
    def __init__(self, id, title, code, description, image_id, rating=None, registrations=None):
        self.id = id
        self.title = title
        self.description = description
        self.code = code
        self.rating = rating
        self.image_id = image_id
        self.registrations = registrations
        
    def getParticipants(self):
        sql = '''
        SELECT COUNT(*) FROM JoinedCourses
        WHERE CourseID = %s
        '''
        return fetchone(sql, (self.id,))[0]
    
    def getRating(self):
        sql = '''SELECT AVG(Rating) FROM CourseRatings WHERE CourseID = %s'''
        return fetchone(sql, (self.id,))[0]
        
    @staticmethod
    def findMatchOR(keys, values):
        sql = "SELECT `Id`, `Title`, `Code`, `Description`, ImageID FROM Courses WHERE "
        where = ' OR '.join(map(lambda k: f"`{k}` = %s", keys))
        print(sql + where)
        result = fetchone(sql + where, values)
        if not result:
            return None
        return Course(*result)

    @staticmethod
    def fetchAll():
        sql = """
        SELECT `ID`, `Title`, `Code`, `Description`, ImageID FROM Courses;
        """
        result = fetchall(sql, as_dict=True)  # Fetch as dictionaries
        if not result:
            return None
        return [
            Course(
                id=row['ID'],
                title=row['Title'],
                code=row['Code'],
                description=row['Description'],
                image_id=row['ImageID']
            ) for row in result
        ]
        
    @staticmethod
    def fetchAllRatings():
        sql = """
        SELECT C.ID, C.Title, C.Code, C.Description, C.ImageID, R.Rating, J.Registrations
        FROM Courses C
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
        result = fetchall(sql, as_dict=True)  # Fetch as dictionaries
        if not result:
            return None
        return [
            Course(
                id=row['ID'],
                title=row['Title'],
                code=row['Code'],
                description=row['Description'],
                image_id=row['ImageID'],
                rating=row.get('Rating'),
                registrations=row.get('Registrations')
            ) for row in result
        ]
    
    @staticmethod
    def fetchJoinedCourses(user_id):
        sql = """
        SELECT Courses.ID, Courses.Title, Courses.Code, Courses.Description, Courses.ImageID, 
               JoinedCourses.JoinDate, JoinedCourses.ViewDate
        FROM JoinedCourses
        JOIN Courses ON JoinedCourses.CourseID = Courses.ID
        WHERE JoinedCourses.UserID = %s
        ORDER BY JoinedCourses.JoinDate DESC
        """
        courses = fetchall(sql, (user_id,), as_dict=True)  # Fetch as dictionaries
        return [
            Course(
                id=row['ID'],
                title=row['Title'],
                code=row['Code'],
                description=row['Description'],
                image_id=row['ImageID']
            ) for row in courses
        ]
    
    def get_img_url(self):
        if not self.image_id:
            return None
        return f'/files/{self.image_id}'
    
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'code': self.code,
            'rating': self.rating,
            'registrations': self.registrations,
            'img_url': self.get_img_url()
        }
