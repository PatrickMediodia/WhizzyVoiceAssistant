import os
import json
import random
from gtts import gTTS

#load responses from response.json
responses = None
with open('responses.json') as f:
    responses = json.load(f)
    
def gtts_speak(audio_string):
    tts = gTTS(text=audio_string, lang='en', tld='com')
    tts.save("audio/speech.mp3")
    
    #play audio
    os.system("mpg123 audio/speech.mp3 >/dev/null 2>&1")
    os.remove("audio/speech.mp3")
    
#usage print(get_response('notFound'))
def get_response(type):
    try:
        return random.choice(responses[type])
    except: 
        return 'Dialog not found'