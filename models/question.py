from models.lowercase import lowercase

class Question(object):
    def __init__(self, id, question, answer, response):
      self.id = id
      self.question = lowercase(question)
      self.answer = lowercase(answer)
      self.response = lowercase(response)