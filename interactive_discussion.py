from text_to_speech import gtts_speak
from speech_to_text import speech_to_text
from API_requests import get_jwt_token, get_lesson_data

"""
Flow
1. get course code
2. get lesson code
3. say "It is all set, tell me when to start"
4. keyword command should be "start" + "type"
    Types:
        a. Introduction
        b. Short Discussion
        c. Trivia
        d. Questions
        e. Conclusion
            
Note: take into account change course code and lesson
    - if change course code, also get lesson
    - if change lesson, make sure to check if lesson is within course code
"""

lesson_data = None

def load_lesson_data():
    global lesson_data
    
    gtts_speak('What is the lesson that you want?')
    
    requested_course = speech_to_text()
    lesson_data = get_lesson_data(get_jwt_token(), requested_course)
    
    if lesson_data is None:
        gtts_speak('No lesson data found')
    else:
        gtts_speak(f'Lesson has been loaded')
        
def start_interactive_discussion(command):
    if lesson_data is None:
        load_lesson_data()
        
    else:
        if 'start' in command:
            if 'introduction' in command:
                gtts_speak(lesson_data.introduction)
                
            elif 'summarize' or 'summarization' or 'summary' in command:
                gtts_speak(lesson_data.summarization)
                
            elif 'trivia' in command:
                pass
            
            elif 'questioning' or 'question' in command:
                pass
                
            elif 'conclusion' in command:
                print(f'Im here {lesson_data.conclusion}')
                gtts_speak(lesson_data.conclusion)
                
            else:
                gtts_speak('Sorry, I cannot process that request')