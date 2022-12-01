from text_to_speech import gtts_speak
from speech_to_text import speech_to_text

interactive_discussion_data = [
    {
        'course_code': 'IT101',
        'lessons': [
            'lesson_code' :
                'trigger': [],
                'dialogs': {
                    'introduction': 'Introduction for lesson 2',
                    'discussion' : [],
                    'trivia': [],
                    'questions': [],
                    'conclusion' : ''
            },
        ]
    }
]

course_code = ""
lesson_code = ""
course_data = None
lesson_data = None

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

def start_interactive_discussion(command):
    global course_code, lesson_code, course_data, lesson_data
    
    if course_code == "":
        gtts_speak('What is the course code that you want?')
        requested_course = speech_to_text()
        
        for course in interactive_discussion_data:
            if requested_course == course['course_code']:
                course_code = requested_course
                course_data = course
                break
        else:
            gtts_speak('Sorry, I cannnot find that course')
            return
        
    if lesson_code = "":
        gtts_speak(f'What is the course lesson that you want for course {course_code}?')
        requested_lesson = speech_to_text()
        
        for key, lesson in course_data['lessons'].items():
            if requested_lesson == key:
                lesson_code = requested_lesson
                lesson_data = lesson
                break
        else:
            gtts_speak('Sorry, I cannnot find that lesson')
            return
        
    if lesson_data not None:
        if 'start' in command:
            if 'introduction' in command:
                gtts_speak('introduction')
            
            elif 'discussion' in command:
                gtts_speak('discussion')
            
            elif 'trivia' in command:
                gtts_speak('trivia')
            
            elif 'questioning' or 'question' in command:
                gtts_speak('questioning')
            
            elif 'conclusion' in command:
                gtts_speak('conclusion')
            
            else:
                gtts_speak('Sorry, I cannot process that request')