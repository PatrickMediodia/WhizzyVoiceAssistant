import os
import speech_recognition as sr
from text_to_speech import gtts_speak

def speech_to_text():
    listener = sr.Recognizer()
    command = ""
    
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source, duration=0.5)
        #listener.energy_threshold = 250
        listener.dynamic_energy_threshold = True
        
        print('Listening to command ...')
        os.system("mpg123 audio/ding_sound_2.mp3 >/dev/null 2>&1")
        
        voice_data = listener.listen(source)
        
        try:
            command = listener.recognize_google(voice_data)
            command = command.lower()
            print(f'Command: {command}')
        except sr.UnknownValueError as e:
            gtts_speak('Sorry, I did not get that')
            print(e)
        except sr.RequestError:
            gtts_speak('Sorry, my speech service is down')
            print(e)
            
    return command