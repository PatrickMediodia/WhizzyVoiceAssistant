import os
import json
import random
from gtts import gTTS

#load responses from response.json
responses = None
with open('responses.json') as f:
    responses = json.load(f)

#usage print(get_response('notFound'))
def get_response(type):
    try:
        return random.choice(responses[type])
    except: 
        return 'Dialog not found'
    
def gtts_speak(audio_string):
    try:
        tts = gTTS(text=audio_string, lang='en', tld='com')
        tts.save("audio/speech.mp3")
        
        #play audio
        os.system("mpg123 audio/speech.mp3 >/dev/null 2>&1")
        os.remove("audio/speech.mp3")
    except AssertionError as e:
        print(e)
    except Exception as e:
        print(e)
        
'''
import pyttsx3

engine = pyttsx3.init('espeak')
engine.setProperty('rate', 150)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[12])

def gtts_speak(audio_string):
    engine.say(audio_string)
    engine.runAndWait()
'''