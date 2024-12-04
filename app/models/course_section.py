from ..db_manager import fetchall, fetchone

class CourseSection:
    
    def __init__(self, id, course_id, title, page_id):
        self.id = id
        self.course_id = course_id
        self.title = title
        self.page_id = page_id
    
    def serialize(self):
        return {
            "id": self.id,
            "course_id": self.course_id,
            "title": self.title,
            "page_id": self.page_id
        }
        
    def findByID(id):
        sql = '''
        SELECT 
        `ID`, `CourseID`, `Title`, `PageID`
        FROM CourseSections
        WHERE ID = %s
        '''
        result = fetchone(sql, (id,))
        if not result: return None
        return CourseSection(*result)
    
    def findCourseSections(courseID):
        sql = '''
        SELECT 
        `ID`, `CourseID`, `Title`, `PageID`
        FROM CourseSections
        WHERE CourseID = %s
        '''
        result = fetchall(sql, (courseID,))
        if not result: return []
        return [CourseSection(*row) for row in result]