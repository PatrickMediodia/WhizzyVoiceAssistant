import Dialog_handler
from Text_to_Speech import gtts_speak
from Speech_to_Text import speech_to_text
from ALSA_handler import noalsaerr
from ControlSmartPlug import turnOnPlug, turnOffPlug

def main():
    with noalsaerr():
        gtts_speak('Hello I am Whizzy, your personal assistant')
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