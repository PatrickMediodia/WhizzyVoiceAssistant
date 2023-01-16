from text_to_speech import gtts_speak
from API_requests import get_user_data
from speech_to_text import speech_to_text
from picovoice.detect_hotword import detect_hotword

"""
Flow
1. get lesson code
2. say "It is all set, tell me when to start"
3. keyword command should be "start" + "type"
    Types:
        a. Introduction
        b. Short Discussion
        c. Trivia
        d. Questions
        e. Conclusion
4. take into account change lesson

Handling Questions and Trivias
1. wait for phrase "start" + "type" where type is "question" or "trivia"
2. (Not saure) when in question and trivia mode, say "start" + "first question"
3. Whizzy will say the question and wait for answer from student
4. Whizzy will reply if the answer is correct or not
5. Teacher can reveal the correct answer "What Whizzy, what is the correct answer"
6. Teacher can tell Whizzy to move on to the next question wth "Hey Whizzy, next question"
7. Teacher can exit Whizzy question mode by saying "Exit" + "question" or "trivia"
"""

lesson_data = None

interactive_discussion_modes = {
    'introduction': ['introduction', 'introduce'],
    'summarization': ['summarization', 'summary'],
    'trivias': ['trivia', 'trivias'],
    'questions' : ['questioning', 'question', 'questions'],
    'conclusion' : ['conclusion'],
}

def load_lesson_data():
    global lesson_data
    
    gtts_speak('What is the lesson that you want?')
    
    requested_course = speech_to_text()
    
    if requested_course == '':
        return
    
    user_data = get_user_data(requested_course)
    
    found = False
    
    #find lesson
    for course in user_data.courses:
        for module in course.modules:
            for lesson in module.lessons:
                if requested_course == lesson.trigger_word:
                    lesson_data = lesson
                    found = True
                    
                    print('Found lesson from trigger word')
                    gtts_speak(f'Lesson has been loaded')
                    break
                
    if not found:
        gtts_speak('No lesson data found')

def load_trivias(trivias):
    gtts_speak('Ok lets start')
    
    current_index = 0
    
    #repeat while in trivia mode
    while True:
        current_trivia = trivias[current_index]
        
        #say the question
        gtts_speak(current_trivia.response)
        
        #repeat until next or previous trivia command
        while True:
            if detect_hotword():
                command = speech_to_text()
                
                #previous question
                if 'previous trivia' in command:
                    if current_index > 0:
                        current_index -= 1
                        current_trivia = trivias[current_index]
                        gtts_speak(current_trivia.response)
                    else:
                        gtts_speak('No previous trivia')
                        
                #next question
                elif 'next trivia' in command:
                    if current_index < len(trivias) - 1:
                        current_index += 1
                        current_trivia = trivias[current_index]
                        gtts_speak(current_trivia.response)
                    else:
                        gtts_speak('No next trivia')
                                       
                #current trivia
                elif 'repeat trivia' in command:
                    gtts_speak(current_trivia.response)
                    
                #exit trivia mode
                elif 'exit' in command:
                    return
                
                else:
                    gtts_speak(f'Sorry I cannot process that request')
                
def load_questions(questions):
    gtts_speak('Ok lets start')
    
    current_index = 0
    
    #repeat while in questioning mode
    while True:
        current_question = questions[current_index]
        
        #say the question
        gtts_speak(current_question.question)
        
        #repeat until next or previous question command
        while True:
            if detect_hotword():
                command = speech_to_text()
                
                #previous question
                if 'previous question' in command:
                    if current_index > 0:
                        current_index -= 1
                        current_question = questions[current_index]
                        gtts_speak(current_question.question)
                    else:
                        gtts_speak('No previous question')
                        
                #next question
                elif 'next question' in command:
                    if current_index < len(questions) - 1:
                        current_index += 1
                        current_question = questions[current_index]
                        gtts_speak(current_question.question)
                    else:
                        gtts_speak('No next question')
                        
                #reveal correct answer
                elif 'correct answer' in command:
                    gtts_speak(f'The correct answer is {current_question.answer}')
                
                #current question
                elif 'repeat question' in command:
                    gtts_speak(current_question.question)
                
                #students answer
                elif 'answer' in command:
                    if current_question.answer in command:
                        gtts_speak(current_question.response)
                    else:
                        gtts_speak('Incorrect answer')
                        
                #exit questioning mode
                elif 'exit' in command:
                    return
                
                else:
                    gtts_speak(f'Sorry I cannot process that request')
                    
def start_interactive_discussion(command):    
    if 'load lesson' in command:
        load_lesson_data()
        
    elif 'current lesson' in command:
        gtts_speak(f'The current lesson is {lesson_data.name}')
    
    elif 'start' in command:
        dialog = ''
        
        #check if a lesson has been loaded
        if lesson_data is None:
            gtts_speak('No lesson selected, please load a lesson')
            return
        
        #check which part of the discussion is being selected
        elif 'introduction' in command: 
            dialog = lesson_data.introduction
         
        elif 'summarization' in command or 'summary' in command:
            dialog = lesson_data.summarization
                
        elif 'trivia' in command:
            if len(lesson_data.trivias) > 0:
                load_trivias(lesson_data.trivias)
                dialog = 'Exiting trivia mode'
           
        elif 'questioning' in command or 'question' in command:
            if len(lesson_data.questions) > 0:
                load_questions(lesson_data.questions)
                dialog = 'Exiting questioning mode'
                
        elif 'conclusion' in command:
            dialog = lesson_data.conclusion
            
        else:
            gtts_speak('Sorry, I cannot process that request')
            return
        
        #tell user if dialog is blank
        if dialog == '':
            dialog = f'No dialog set for that part of the discussion'
            
        gtts_speak(dialog)
            
    else:
        gtts_speak('Sorry, I cannot process that request')