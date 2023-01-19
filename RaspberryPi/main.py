#Main Imports
import time
import threading
from ALSA_handler import noalsaerr
from API_requests import authenticate
from text_to_speech import gtts_speak
from speech_to_text import speech_to_text
from whizzy_avatar import initialize_avatar
from picovoice.detect_hotword import detect_hotword

#Web Searching
from web_searching import start_google_assistant

#Interactive Discussion
from interactive_discussion import start_interactive_discussion

#Smart Controls
from smart_controls.windows_script import login_terminal
from smart_controls.smart_controls import initialize_devices, start_smart_controls

modes = (
    'web searching',
    'smart control',
    'interactive discussion'
)

mode_map = {
    'web searching': start_google_assistant,
    'smart control': start_smart_controls,
    'interactive discussion': start_interactive_discussion
}

#temporary credentials
USERNAME = 'faculty1'
PASSWORD = '123456'

MAC_ADDRESS = '34.02.86.F8.DA.09' #'B8.97.5A.C0.EA.09'

current_mode = modes[1]

def change_mode(current_mode, command):
    if 'switch' in command or 'change' in command:
        for mode in modes:
            if mode in command and current_mode != mode:
                return mode
    return current_mode

def main():
    global current_mode
    account = authenticate(USERNAME, PASSWORD)
    
    if account == None:
        gtts_speak('Incorrect credentials')
        print('Incorrect credentials')
        return

    #start after authentication
    #initializing devices in the classroon
    threading.Thread(target=initialize_devices, daemon=True).start()

    #turn on professor terminal using WOL packet
    #start_terminal(MAC_ADDRESS)
    #start_terminal('68.F7.28.E3.B7.31')
    
    #login to windows
    #Local credentials, connect to API
    login_terminal('Pat', 'Admin1234@', 'DESKTOP-0K06L79')
    
    #start new thread for avatar
    threading.Thread(target=initialize_avatar, daemon=True).start()
    time.sleep(5)
    gtts_speak('Hello I am Whizzy, your personal assistant')
    
    with noalsaerr():
        while True:
            print(f'Current mode: {current_mode}')
            if detect_hotword():
                command = speech_to_text()
                
                #command is empty, ignore
                if command == '':
                    continue
                
                #change modes
                new_mode = change_mode(current_mode, command)
                if new_mode != current_mode:
                    current_mode = new_mode
                    gtts_speak(f'Switched to {new_mode}')
                
                #to get the current mode of Whizzy
                elif "current" and "mode" in command:
                    gtts_speak(f"Currently I am in the {current_mode} mode")
                
                #send command to current mode
                else:
                    mode_map[current_mode](command)
                    
if __name__ == '__main__':
    main()