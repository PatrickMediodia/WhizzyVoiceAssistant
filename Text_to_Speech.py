import os
import pyttsx3
from gtts import gTTS

def gtts_speak(speech):
    tts = gTTS(text=speech, lang='en', tld='com')
    tts.save("audio/speech.mp3")
    os.system("mpg123 audio/speech.mp3")

"""
#User in main method
with noalsaerr():

#Initialize in File
pyttsx3_engine = Text_to_Speech.initialize_pyttsx3()

#Usage
pyttsx3_engine.say('Hello I am Whizzy, your personal assistant')
pyttsx3_engine.runAndWait()
        
def initialize_pyttsx3():
    engine = pyttsx3.init('espeak')
    #set voice type
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[11].id)

    #set talking rate
    engine.setProperty('rate', 100)
    
    return engine
"""