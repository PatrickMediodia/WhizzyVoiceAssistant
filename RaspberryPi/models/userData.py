from models.section import Section

class UserData:
    def __init__(self, id, username, email, sections):
        self.id = id
        self.username = username
        self.email = email
        self.sections = [ Section(**section) for section in sections ]
