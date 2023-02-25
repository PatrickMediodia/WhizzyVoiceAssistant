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

#google text to speech (online)
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
#festival, sound ok offline but is slow
def gtts_speak(audio_string):
    os.system(f'echo "{audio_string}" | festival --tts')
'''

'''
#PYTTSX3, sounds bad offline but is fast
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 125)

voices = engine.getProperty('voices')
print(voices)
engine.setProperty('voice', voices[12].id)

def gtts_speak(audio_string):
    engine.say(audio_string)
    engine.runAndWait()
'''

'''
#mimic3, sounds the best offline but is super slow
def gtts_speak(audio_string):
    os.system(f'mimic3 --voice en_US/cmu-arctic_low "{audio_string}" > audio/output.wav')

    os.system("mpg123 audio/output.wav >/dev/null 2>&1")
    os.remove("audio/output.wav")
'''
