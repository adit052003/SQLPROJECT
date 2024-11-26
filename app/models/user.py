from flask_login import UserMixin
from ..db_manager import fetchone

class User(UserMixin):
    
    def __init__(self, id, first_name, last_name, email, password):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        
    def findMatchOR(keys, values):
        sql = "SELECT `Id`, `FirstName`, `LastName`, `Email`, `Password` FROM Users WHERE "
        where = ' OR '.join(map(lambda k: f"`{k}` = %s", keys))
        print(sql + where)
        result = fetchone(sql + where, values)
        if not result: return None
        return User(*result)
    
    def hasJoinedCourse(self, courseID):
        sql = '''
        SELECT * FROM JoinedCourses
        WHERE UserID = %s AND CourseID = %s
        '''
        return bool(fetchone(sql, (self.id, courseID)))