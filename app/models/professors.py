from ..db_manager import fetchall

class Professor():
    
    def __init__(self, id, first_name, last_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        
    def getAll():
        sql = "SELECT `Id`, `FirstName`, `LastName` FROM Professors"
        result = fetchall(sql, ())
        if not result: return None
        return [Professor(*row) for row in result]
    
    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name
        }