import os
import speech_recognition as sr

def speech_to_text():
    listener = sr.Recognizer()
    command = ""
    
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source)
        
        print('Say command')
        os.system("mpg123 audio/ding_sound_2.mp3 >/dev/null 2>&1")
        
        voice = listener.listen(source)
                
        try:
            command = listener.recognize_google(voice)
            print(f'Command: {command}')
        
        except Exception as e:
            print(e)
            pass
    
    return command