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

import time
from num2words import num2words
from API_requests import get_user_data
from text_to_speech import get_response
from picovoice.detect_hotword import detect_hotword
from speech_to_text import speech_to_text, get_command
from whizzy_avatar import set_mode_text, set_lesson_text, whizzy_speak, set_show_mic_state

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
    set_mode_text('Interactive Discussion - Load Lesson')
    
    whizzy_speak('What is the lesson that you want?')
    time.sleep(1)
    requested_course = speech_to_text()
    
    if requested_course == '':
        return
    
    user_data = get_user_data()
    found = False
    
    #check if courses are available
    if len(user_data.sections) < 1:
        print('\nNo lesson data on this account')
        whizzy_speak('I was not able to get any lesson data on this account')
        found = True

    #find lesson
    for section in user_data.sections:
        for module in section.modules:
            for lesson in module.lessons:
                if requested_course == lesson.trigger_word:
                    lesson_data = lesson
                    found = True
                    
                    print('Found lesson from trigger word')
                    whizzy_speak(f'Lesson has been loaded')
                    
                    set_lesson_text(f'{lesson_data.name}')
                    set_mode_text('Interactive Discussion')
                    
                    break
                
    if not found:
        whizzy_speak(get_response('lessonDataNotFound'))
        set_mode_text('Interactive Discussion')
        
def load_trivias(trivias):
    whizzy_speak(get_response('startDialog'))
    
    current_index = 0
    dialog = trivias[current_index].response
    
    #repeat until next or previous trivia command
    while True:
        set_mode_text(f'Interactive Discussion - Trivia - {current_index+1}/{len(trivias)}')   
        whizzy_speak(dialog)
        
        # accepting triggger of input
        set_show_mic_state(True)
        
        if detect_hotword():
            command = speech_to_text()

            #cancel the current command
            if 'cancel' in command:
                dialog = get_response('cancel')
                
            #previous trivia
            elif 'previous' in command and 'trivia' in command:
                if current_index > 0:
                    current_index -= 1
                    dialog = trivias[current_index].response
                else:
                    dialog = 'No previous trivia'
                    
            #next trivia
            elif 'next' in command and 'trivia' in command:
                if current_index < len(trivias) - 1:
                    current_index += 1   
                    dialog = trivias[current_index].response
                else:
                    dialog = 'No next trivia'
                                       
            #current trivia
            elif 'repeat' in command and 'trivia' in command:
                dialog = trivias[current_index].response
            
            #move to another trivia
            elif get_command('switch', command) and 'trivia' in command:
                for number in range(1, len(trivias)+1):
                    #check if number in number or word form is in command
                    if str(number) in command or num2words(number) in command:
                        current_index = number - 1
                        dialog = trivias[current_index].response
                        break
                    
            #exit trivia mode
            elif 'exit' in command and 'trivia' in command:
                return
                
            else:
                dialog = get_response('notFound')
                
def load_questions(questions):
    whizzy_speak(get_response('startDialog'))
    
    current_index = 0
    dialog = questions[current_index].question
         
    #repeat until next or previous question command
    while True:
        set_mode_text(f'Interactive Discussion - Questions - {current_index+1}/{len(questions)}') #change text
        whizzy_speak(dialog)
        
        set_show_mic_state(True)
        
        if detect_hotword():
            command = speech_to_text()
            
            #cancel the current command
            if 'cancel' in command:
                dialog = get_response('cancel')
            
            #checking for none dialogs
            elif 'answer' in command and questions[current_index].answer is None:
                dialog = 'No answer set for this question'
                
            #previous question
            elif 'previous' in command and 'question' in command:
                if current_index > 0:
                    current_index -= 1
                    dialog = questions[current_index].question
                else:
                    dialog = 'No previous question'
                    commence
            #next question
            elif 'next' in command and 'question' in command:
                if current_index < len(questions) - 1:
                    current_index += 1
                    dialog = questions[current_index].question
                else:
                    dialog = 'No next question'

            #move to another question
            elif get_command('switch', command) and 'question' in command:
                for number in range(1, len(questions)+1):
                    #check if number in number or word form is in command
                    if str(number) in command or num2words(number) in command:
                        current_index = number - 1
                        dialog = questions[current_index].question
                        break
                    
            #current question
            elif 'repeat' in command and 'question' in command:
                dialog = questions[current_index].question
    
            #reveal correct answer
            elif 'correct' in command and 'answer' in command:
                dialog = f'The correct answer is {questions[current_index].answer}'
                
            #students answer
            elif 'answer' in command:
                if questions[current_index].answer in command:
                    dialog = questions[current_index].response
                else:
                    dialog = get_response('incorrectAnswer')
                    
            #exit questioning mode
            elif 'exit' in command and 'question' in command:
                return
            
            else:
                dialog = get_response('notFound')
                
def start_interactive_discussion(command):
    global lesson_data
    
    if 'load' in command and 'lesson' in command:
        load_lesson_data()
    
    elif lesson_data is None:
        whizzy_speak(get_response('noLesson'))
        return
    
    elif 'current' in command and 'lesson' in command:
        whizzy_speak(f'The current lesson is {lesson_data.name}')
        
    elif 'remove' in command and 'lesson' in command:
        lesson_data = None
        
        whizzy_speak(f'The current lesson has been removed')
        set_lesson_text('Please load a lesson')
        
    elif get_command('start', command):
        dialog = ''
        
        #check which part of the discussion is being selected
        if 'introduction' in command:
            set_mode_text('Interactive Discussion - Introduction')
            dialog = lesson_data.introduction
            
        elif 'summarization' in command or 'summary' in command:
            set_mode_text('Interactive Discussion - Summary')
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
            set_mode_text('Interactive Discussion - Conclusion')
            dialog = lesson_data.conclusion

        else:
            dialog = get_response('notFound')
            
        #tell user if dialog is blank
        if dialog == '' or dialog == None:
            dialog = f'No dialog set for that part of the discussion'
        
        whizzy_speak(dialog)
        set_mode_text('Interactive Discussion')
        
    else:
        whizzy_speak(get_response('notFound'))
