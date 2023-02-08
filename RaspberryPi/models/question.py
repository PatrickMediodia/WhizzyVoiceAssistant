from models.lowercase import lowercase

class Question(object):
    def __init__(self, id, question, answer, response):
      self.id = id
      self.question = question
      self.answer = lowercase(answer)
      self.response = response