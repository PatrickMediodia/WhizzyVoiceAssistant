from models.module import Module

class Section(object):
    def __init__(self, id, name, createdAt, updatedAt, publishedAt, start_time, end_time, availability, modules, course):
        self.id = id
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.availability = availability
        self.modules = [ Module(**module) for module in modules ]
