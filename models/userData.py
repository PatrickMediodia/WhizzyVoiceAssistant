from models.course import Course

class UserData:
    def __init__(self, id, username, email, courses):
        self.id = id
        self.username = username
        self.email = email
        self.courses = [ Course(**course) for course in courses ]