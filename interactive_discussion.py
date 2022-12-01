from text_to_speech import gtts_speak
from speech_to_text import speech_to_text

interactive_discussion_data = [
    {
        'course_code' : 'IT101',
        'course_title' : 'Capstone',
        'lessons': [
            {
                'lesson_code' : 'Code of lesson 1',
                'lesson_title' : 'Title of lesson 1',
                'dialogs': {
                    'introduction': 'Introduction for lesson 2',
                    'discussion' : [],
                    'trivia': [],
                    'questions': [],
                    'conclusion' : ''
                }
            },
        ]
    },
]

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

def get_lesson_data():
    global course_data, lesson_data
    
    if course_data is None:
        gtts_speak('What is the course that you want?')
        requested_course = speech_to_text()
            
        for course in interactive_discussion_data:
            if requested_course in course['course_title'].lower():
                course_data = course
                lesson_data = None
                gtts_speak(f'{course["course_title"]} has been selected')
                break
        else:
            gtts_speak('Sorry, I cannnot find that course')
            return

    if lesson_data is None:
        gtts_speak(f'What is the lesson that you want for the course, {course_data["course_title"]}?')
        requested_lesson = speech_to_text()
        
        for lesson in course_data['lessons']:
            if requested_lesson in lesson['lesson_title'].lower():
                lesson_data = lesson
                gtts_speak(f'{lesson["lesson_title"]} has been selected')
                break
        else:
            gtts_speak('Sorry, I cannnot find that lesson')
            return
        
    return lesson_data

def start_interactive_discussion(command):
    global lesson_data
    
    if lesson_data is None:
        lesson_data = get_lesson_data()
    
    else:
        if 'start' in command:
            if 'introduction' in command:
                gtts_speak(lesson_data['dialogs']['introduction'])
                
            elif 'discussion' in command:
                gtts_speak(lesson_data['dialogs']['discussion'])
                
            elif 'trivia' in command:
                gtts_speak(lesson_data['dialogs']['trivia'])
                
            elif 'questioning' or 'question' in command:
                gtts_speak(lesson_data['dialogs']['questioning'])
                
            elif 'conclusion' in command:
                gtts_speak(lesson_data['dialogs']['conclusion'])
                
            else:
                gtts_speak('Sorry, I cannot process that request')