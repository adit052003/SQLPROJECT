from ..db_manager import fetchone
class Page:
    def __init__(self, id, course_id, title, section_index, content, created_at, updated_at):
        self.id = id
        self.course_id = course_id
        self.title = title
        self.section_index = section_index
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def fetch_page(course_id, page_id):
        sql = "SELECT * FROM Pages WHERE CourseID = %s AND ID = %s"
        return fetchone(sql, (course_id, page_id))
