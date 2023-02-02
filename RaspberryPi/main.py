#Main Imports
import os
import time
import threading
from ALSA_handler import noalsaerr
from API_requests import authenticate
from speech_to_text import speech_to_text
from picovoice.detect_hotword import detect_hotword
from whizzy_avatar import initialize_avatar, set_mode_text, whizzy_speak

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
        print('Incorrect credentials')
        return
    
    #start after authentication
    #initializing devices in the classroom
    print('Initializing devices ......\n')
    initialize_devices()
    
    #new thread for avatar
    initialize_avatar_thread = threading.Thread(target=initialize_avatar, daemon=True)
    initialize_avatar_thread.name = 'Initialize avatar'
    initialize_avatar_thread.start()
    
    set_mode_text(current_mode)
    
    #initial speech of Whizzy
    time.sleep(5)
    whizzy_speak('Hello I am Whizzy, your classroom assistant')
    
    with noalsaerr():
        while True:
            print(f'\nCurrent mode: {current_mode}')
            print(threading.enumerate())
            
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