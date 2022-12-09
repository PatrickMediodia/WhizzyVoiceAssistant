from models.question import Question
from models.trivia import Trivia

class Lesson(object):
    def __init__(self, id, responses, createdAt, updatedAt, publishedAt, name):
      self.id = id
      self.name = name
      self.trigger_word = responses['trigger_word']
      self.introduction = responses['introduction']
      self.summarization = responses['summarization']
      self.questions = [ Question(**question) for question in responses['questions'] ] 
      self.trivias = [ Trivia(**trivia) for trivia in responses['trivias'] ] 
      self.conclusion = responses['conclusion']