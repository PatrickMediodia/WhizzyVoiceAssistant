import Dialog_handler
from ALSA_handler import noalsaerr
from Text_to_Speech import gtts_speak
from Speech_to_Text import speech_to_text
from ControlSmartPlug import turnOnPlug, turnOffPlug
from detect_hotword import detect_hotword

def main():
    gtts_speak('Hello I am Whizzy, your personal assistant')
    
    with noalsaerr():
        while True:
            detected = detect_hotword()
            
            if detected:
                command = speech_to_text()
                
                if 'turn' and 'plug' in command:
                    if 'off' in command: 
                        turnOffPlug()
                        gtts_speak('Plug turned off')
                    elif 'on' in command:
                        turnOnPlug()
                        gtts_speak('Plug turned on')
                
if __name__ == '__main__':
    main()