from flask_login import UserMixin
from ..db_manager import fetchone

class User(UserMixin):
    
    def __init__(self, **data):
        self.id = data['Id']
        self.first_name = data['FirstName']
        self.last_name = data['LastName']
        self.email = data['Email']
        self.password = data['Password']
        
    def findMatchOR(keys, values):
        sql = "SELECT `Id`, `FirstName`, `LastName`, `Email`, `Password` FROM Users WHERE "
        where = ' OR '.join(map(lambda k: f"`{k}` = %s", keys))
        print(sql + where)
        result = fetchone(sql + where, values)
        if not result: return None
        return User(**result)
    
    def hasJoinedCourse(self, courseID):
        sql = '''
        SELECT * FROM JoinedCourses
        WHERE UserID = %s AND CourseID = %s
        '''
        return bool(fetchone(sql, (self.id, courseID)))