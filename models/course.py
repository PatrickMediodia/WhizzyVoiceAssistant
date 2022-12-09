from models.module import Module

class Course(object):
    def __init__(self, id, course_name, createdAt, updatedAt, publishedAt, acronym, term, modules):
        self.id = id
        self.course_name = course_name
        self.acronym = acronym
        self.term = term
        self.modules = [ Module(**module) for module in modules ]