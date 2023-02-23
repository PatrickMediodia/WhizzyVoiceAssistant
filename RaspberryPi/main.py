#Main Imports
import os
import time
import datetime
import threading
from ALSA_handler import noalsaerr
from text_to_speech import get_response
from picovoice.detect_hotword import detect_hotword
from speech_to_text import speech_to_text, get_command
from interactive_discussion import start_interactive_discussion
from google_assistant.google_assistant import start_google_assistant
from API_requests import get_logged_in, logout_user, classroom_log, get_user_modes
from whizzy_avatar import initialize_avatar, set_mode_text, whizzy_speak, set_show_mic_state
from smart_controls.smart_controls import initialize_devices, start_smart_controls, turn_off_devices

modes = {
    'web_searching': {
        'keyword' : 'web searching',
        'function' : start_google_assistant
    },
    'smart_controls': {
        'keyword' : 'smart control',
        'function' : start_smart_controls
    },
    'interactive_discussion': {
        'keyword' : 'interactive discussion',
        'function' : start_interactive_discussion
    }
}

#new thread for avatar
initialize_avatar_thread = threading.Thread(target=initialize_avatar, daemon=True)
initialize_avatar_thread.name = 'Initialize avatar'
initialize_avatar_thread.start()

set_mode_text('Waiting for login')

date = None
start_time = None
current_mode = None

new_login = True
devices_initialized = False

def get_time():
    time = datetime.datetime.now().strftime("%H:%M:%S.%f")
    return time[:-3]

def change_mode(command):
    global current_mode, available_modes
    
    if get_command('switch', command) is False:
        return False
    
    available_modes = get_user_modes()
    
    for mode, mode_object in modes.items():
        
        #get synonyms from command dictionary
        if get_command(mode, command):
            
            #check if different from current mode
            if current_mode['keyword'] != mode_object['keyword']:
                
                #new mode is enabled
                if available_modes[mode] is True:
                    current_mode = mode_object
                    set_mode_text(mode_object['keyword'])
                    whizzy_speak(f'Switched to {mode_object["keyword"]}')
                
                #new mode is disabled
                elif available_modes[mode] is False:
                    whizzy_speak(f'{mode_object["keyword"].capitalize()} is disabled')
                    
            #check if same as current mode
            elif current_mode['keyword'] == mode_object['keyword']:
                whizzy_speak(f'Already in {current_mode["keyword"]} mode')

            return True
        
    return False

def login():
    global current_mode, date, start_time, available_modes, devices_initialized

    #get date and time of login
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    start_time = get_time()
    
    #start after authentication
    set_mode_text('Logged in')
    whizzy_speak('Logged in, welcome')
    
    available_modes = get_user_modes()
    if available_modes is None:
        whizzy_speak('No available modes, please enable a mode')
        set_mode_text('No available modes')
        current_mode = None
        return
    
    elif available_modes['smart_controls'] is True:
        #initializing devices in the classroom
        print('\nInitializing devices ......\n')
        initialize_devices()
        
        current_mode = modes['smart_controls']
        devices_initialized = True
        
    elif available_modes['web_searching'] is True:
        current_mode = modes['web_searching']
        
    elif available_modes['interactive_discussion'] is True:
        current_mode = modes['interactive_discussion']
        
    else:
        whizzy_speak('No available modes, please enable a mode')
        set_mode_text('No available modes')
        current_mode = None
        return
    
    #initial speech of Whizzy
    time.sleep(5)
    whizzy_speak(get_response('entrance'))
    set_mode_text(current_mode['keyword'])
    
def logout():
    global current_mode, new_login, date, start_time, end_time, available_modes, devices_initialized
    
    #whizzy speaks
    whizzy_speak(get_response('exit'))
    
    #turn off devices
    turn_off_devices()
    logout_user()
    
    #get logout time and record log
    end_time = get_time()
    classroom_log(date, start_time, end_time)
    
    #reset values
    date = None
    start_time = None
    end_time = None
    current_mode = None
    available_modes = None
    
    new_login = True
    devices_initialized = False
    
    print('\nLogged out')
    set_show_mic_state(False)
    set_mode_text('Waiting for login')
    
def main():
    global new_login
    
    #check if logged into classroom
    if not get_logged_in():
        if new_login:
            print('\nWaiting for login .....\n')
            new_login = False
        return
    
    login()
    
    while True:
        print(f'\n{threading.enumerate()}')
        print(f'\nCurrent mode: {current_mode["keyword"]}')
            
        # accepting triggger of input
        set_show_mic_state(True)
        
        #waiting for hotword
        if detect_hotword():
            command = speech_to_text()
            
            #command is empty, ignore
            if command == '':
                #whizzy_speak(get_response('unknownValueError')) (uncomment if using vosk)
                continue
            
            #cancel the current command
            elif 'cancel' in command:
                whizzy_speak(get_response('cancel'))

            #change modes
            elif change_mode(command) == True:
                continue
            
            #to get the current mode of Whizzy
            elif 'current' and 'mode' in command:
                whizzy_speak(f'Currently I am in the {current_mode} mode')
                
            #exit message and turn off devices
            elif command == 'logout':
                logout()                
                break
            
            #send command to current mode
            else:
                #check if there are is no current mode
                if current_mode is None:
                    whizzy_speak('No available modes, please enable a mode')
                    continue
                
                current_mode['function'](command)
                
if __name__ == '__main__':
    with noalsaerr():
        while True:
            time.sleep(3)
            main()