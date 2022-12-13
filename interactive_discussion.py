from text_to_speech import gtts_speak
from speech_to_text import speech_to_text
from picovoice.detect_hotword import detect_hotword
from API_requests import get_jwt_token, get_lesson_data

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

def load_lesson_data():
    global lesson_data
    
    gtts_speak('What is the lesson that you want?')
    
    requested_course = speech_to_text()
    lesson_data = get_lesson_data(get_jwt_token(), requested_course)
    
    if lesson_data is None:
        gtts_speak('No lesson data found')
    else:
        gtts_speak(f'Lesson has been loaded')

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
                
                #students answer
                if 'answer' in command:
                    if current_question.answer in command:
                        gtts_speak(current_question.response)
                    else:
                        gtts_speak('Incorrect answer')
                        
                #previous question
                elif ('previous' and 'question') in command:
                    current_index -= 1
                    
                #next question
                elif ('next' and 'question') in command:
                    current_index += 1
                
                #reveal correct answer
                elif ('correct' and 'answer') in command:
                    gtts_speak(f'The correct answer is {current_question.answer}')
                
                #exit questioning mode
                elif 'exit' in command:
                    gtts_speak(f'Exiting questioning mode')
                    return

def start_interactive_discussion(command):
    if 'load' and 'lesson' in command:
        load_lesson_data()
    
    elif lesson_data is None:
        gtts_speak('No lesson selected, please load a lesson')
    
    elif 'start' in command:
        if 'introduction' in command:
            gtts_speak(lesson_data.introduction)
                
        elif ('summarize' or 'summarization' or 'summary') in command:
            gtts_speak(lesson_data.summarization)
                
        elif 'trivia' in command:
            print(f'Im in the trivia')
           
        elif ('questioning' or 'question') in command:
            load_questions(lesson_data.questions)
                
        elif 'conclusion' in command:
            gtts_speak(lesson_data.conclusion)
            
        else:
            gtts_speak('Sorry, I cannot process that request')
            
    else:
        gtts_speak('Sorry, I cannot process that request')