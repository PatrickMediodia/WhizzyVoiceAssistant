import os
import json
import speech_recognition as sr
from text_to_speech import get_response
from whizzy_avatar import set_mic_state, whizzy_speak, set_show_mic_state

#load word synonyms from command_dictionary.json
command_dictionary = None
with open('command_dictionary.json') as f:
    command_dictionary = json.load(f)
    
def get_command(type, command):
    try:
        synonyms = command_dictionary[type]
        for synonym in synonyms:
            if synonym in command:
                return True
        return False
    except: 
        return False
    
def replace_command(type, command):
    synonyms = command_dictionary[type]
    new_command = command
    
    for synonym in synonyms:
        if synonym in command:
            new_command = command.replace(synonym, type)
            
    return new_command

def speech_to_text():
    set_show_mic_state(True)
    
    listener = sr.Recognizer()
    command = ''
    
    with sr.Microphone() as source:
        #play sound to indicate start talking
        print('Listening to command ...')
        os.system("mpg123 audio/ding_sound.mp3 >/dev/null 2>&1")
        
        try:
            #automatically sets the energy threshold
            listener.adjust_for_ambient_noise(source, duration=1)
            
            set_mic_state(True)
                          
            voice_data = listener.listen(source, timeout=10, phrase_time_limit=8)
            
            command = listener.recognize_google(voice_data)
            command = command.lower()
            print(f'Command: {command}')
        except sr.UnknownValueError as e:
            whizzy_speak(get_response('unknownValueError'))
            print(e)
        except sr.RequestError as e:
            whizzy_speak('Sorry, my speech service is down')
            print(e)
        except sr.WaitTimeoutError as e:
            whizzy_speak(get_response('unknownValueError'))
            print(e)
        except Exception as e:
            whizzy_speak('There seems to be a problem with my speech recognition')
            print(e)
        
        set_mic_state(False)
        set_show_mic_state(False)
        
    return command

'''
import os
import json
import pyaudio
from ALSA_handler import noalsaerr
from text_to_speech import get_response
from vosk import Model, KaldiRecognizer, SetLogLevel
from whizzy_avatar import set_mic_state, whizzy_speak, set_show_mic_state

with noalsaerr():
    SetLogLevel(-1) #supress logs
    print('Loading vosk model ......\n')
    
    model = Model(r'/home/whizzy/env/WhizzyVoiceAssistant/RaspberryPi/vosk_models/vosk_model_medium')
    recognizer = KaldiRecognizer(model, 16000)
    mic = pyaudio.PyAudio()
    
def speech_to_text():
    set_show_mic_state(True)
    
    stream = mic.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=8192
    )
    
    set_mic_state(True)
    
    #play sound to indicate start talking
    print('Listening to command ...')
    os.system("mpg123 audio/ding_sound.mp3 >/dev/null 2>&1")
    
    stream.start_stream()
    
    while True:
        data = stream.read(4096)
        
        if recognizer.AcceptWaveform(data):
            set_mic_state(False)
            set_show_mic_state(False)
            
            response = recognizer.Result()
            stream.stop_stream()
            stream.close()
            
            text = json.loads(response)['text']
            print(f'Command: {text}')
         
            return text
'''