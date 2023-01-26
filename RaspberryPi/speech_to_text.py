import os
import threading
import speech_recognition as sr
from whizzy_avatar import set_mic_state
from text_to_speech import gtts_speak, get_response

def speech_to_text():
    listener = sr.Recognizer()
    command = ""
    
    with sr.Microphone() as source:
        #play sound to indicate start talking
        print('Listening to command ...')
        os.system("mpg123 audio/ding_sound.mp3 >/dev/null 2>&1")
        
        set_mic_state(True)
        
        #automatically sets the energy threshold
        listener.adjust_for_ambient_noise(source, duration=0.5)
        voice_data = listener.listen(source)
        
        set_mic_state(False)
        
        try:
            command = listener.recognize_google(voice_data)
            command = command.lower()
            print(f'Command: {command}')
        except sr.UnknownValueError as e:
            gtts_speak(get_response('unknownValueError'))
            print(e)
        except sr.RequestError as e:
            gtts_speak('Sorry, my speech service is down')
            print(e)
            
    return command