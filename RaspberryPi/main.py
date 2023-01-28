#Main Imports
import os
import time
import threading
from ALSA_handler import noalsaerr
from API_requests import authenticate
from speech_to_text import speech_to_text
from picovoice.detect_hotword import detect_hotword
from whizzy_avatar import initialize_avatar, set_mode_text, whizzy_speak

#Web Searching
from web_searching import start_google_assistant

#Interactive Discussion
from interactive_discussion import start_interactive_discussion

#Smart Controls
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
USERNAME = os.environ.get('FACULTY_USERNAME')
PASSWORD = os.environ.get('FACULTY_PASSWORD')

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
    #new thread for avatar
    threading.Thread(target=initialize_avatar, daemon=True).start()
    set_mode_text(current_mode)
    
    #initial speech of Whizzy
    time.sleep(5)
    whizzy_speak('Hello I am Whizzy, your personal assistant')
    
    #whizzy_speak('this is an example of a super long string that needs to be cut in order to have subtitles but I am not sure if this is going to work. Hello, test test test this is another test')

    #initializing devices in the classroon
    threading.Thread(target=initialize_devices, daemon=True).start()
    
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
                    set_mode_text(current_mode)
                    whizzy_speak(f'Switched to {new_mode}')
                
                #to get the current mode of Whizzy
                elif "current" and "mode" in command:
                    whizzy_speak(f"Currently I am in the {current_mode} mode")
                
                #send command to current mode
                else:
                    mode_map[current_mode](command)

if __name__ == '__main__':
    main()