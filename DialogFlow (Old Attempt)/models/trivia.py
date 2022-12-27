from models.lowercase import lowercase

class Trivia(object):
    def __init__(self, id, keyword, response):
      self.id = id
      self.keyword = lowercase(keyword)
      self.response = lowercase(response)