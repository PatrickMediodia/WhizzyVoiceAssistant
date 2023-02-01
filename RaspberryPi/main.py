#Main Imports
import os
import time
import threading
from ALSA_handler import noalsaerr
from API_requests import authenticate
from speech_to_text import speech_to_text
from picovoice.detect_hotword import detect_hotword
from whizzy_avatar import initialize_avatar, set_mode_text, whizzy_speak, get_avatar_state

#Interactive Discussion
from interactive_discussion import start_interactive_discussion

#Web Searching
from google_assistant.google_assistant import start_google_assistant

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

current_mode = modes[0]

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
    
    #initializing devices in the classroon
    threading.Thread(target=initialize_devices, daemon=True).start()
    
    with noalsaerr():
        while True:
            print(f'\nCurrent mode: {current_mode}')
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