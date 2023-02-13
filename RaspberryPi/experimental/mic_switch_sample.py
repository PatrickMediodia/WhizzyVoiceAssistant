import os
import speech_recognition as sr

device_index = None

def speech_to_text():
    mic = sr.Microphone(device_index=device_index)
    listener = sr.Recognizer()
    command = ""
    
    with mic as source:
        print(f'Device index: {device_index}')
        #play sound to indicate start talking
        print('Listening to command ...')
        os.system("mpg123 audio/ding_sound.mp3 >/dev/null 2>&1")
        
        #automatically sets the energy threshold
        listener.adjust_for_ambient_noise(source, duration=1)
                      
        voice_data = listener.listen(source, phrase_time_limit=10)
        
        try:
            command = listener.recognize_google(voice_data)
            command = command.lower()
            print(f'Command: {command}')
        except sr.UnknownValueError as e:
            print('I did not get any value')
            print(e)
        except sr.RequestError as e:
            print('Speech service is down')
            print(e)
            
    return command
    
def use_secondary_mic():
    global device_index
    
    device_index = 1

def use_primary_mic():
    global device_index
    
    device_index = 2
    
#use_primary_mic()
#print('Getting input from primary mic ......')
#speech_to_text()

#import time
#time.sleep(5)
print(sr.Microphone.list_microphone_names())
use_secondary_mic()
print('Getting input from secondary mic ......')
speech_to_text()