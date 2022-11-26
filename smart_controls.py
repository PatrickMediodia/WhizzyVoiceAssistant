import time
from PyP100 import PyP100
from text_to_speech import gtts_speak
from speech_to_text import speech_to_text

#TABO credentails
username = 'whizzyassistant@gmail.com'
password = 'Admin1234@'

# IP of Smart Plug, Account Credentials
p100 = PyP100.P100('192.168.1.9', username, password)

#initialize
p100.handshake()
p100.login()

def start_smart_controls():
    #temporary
    command = speech_to_text()
    
    if 'turn' and 'plug' in command:
        #add if already on or off
        if 'off' in command:
            turnOffPlug()
            gtts_speak('Plug turned off')
        elif 'on' in command:
            turnOnPlug()
            gtts_speak('Plug turned on')
    else:
        gtts_speak('Command not found')
        
def device_state(): 
    print(p100.getDeviceInfo()['result']['device_on'])

def turnOnPlug():
    p100.turnOn()
    print('Turned On')
    
def turnOffPlug():
    p100.turnOff()
    print('Turned Off')