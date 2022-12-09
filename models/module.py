from models.lesson import Lesson

class Module(object):
    def __init__(self, id, createdAt, updatedAt, publishedAt, name, lessons):
        self.id = id
        self.name = name
        self.lessons = [ Lesson(**lesson) for lesson in lessons ]