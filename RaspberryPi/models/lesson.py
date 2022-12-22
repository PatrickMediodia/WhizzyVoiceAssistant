from models.lowercase import lowercase
from models.trivia import Trivia
from models.question import Question

class Lesson(object):
    def __init__(self, id, name, createdAt, updatedAt, publishedAt, trigger_word, introduction, summarization, conclusion, trivias, questions):
      self.id = id
      self.name = name
      self.trigger_word = lowercase(trigger_word)
      self.introduction = introduction
      self.summarization = summarization
      self.questions = [ Question(**question) for question in questions] 
      self.trivias = [ Trivia(**trivia) for trivia in trivias] 
      self.conclusion = conclusion