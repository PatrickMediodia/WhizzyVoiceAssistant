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
from whizzy_avatar import initialize_avatar, set_mode_text, whizzy_speak, set_show_mic_state
from smart_controls.smart_controls import initialize_devices, start_smart_controls, turn_off_devices
from API_requests import get_logged_in, logout_user, classroom_log, get_user_modes, get_web_command, clear_web_command

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

def web_command(command_dictionary):
    while True:
        if command_dictionary['command'] != '':
            return
            
        response = get_web_command()
        if response != None and response != '':
            command_dictionary['command'] = response
            #clear user command after execution
            clear_web_command()
            return
            
        time.sleep(2)
        
def get_user_command():
    command_dictionary = {'command' : ''}
    
    #start thread for getting command from web
    user_command_thread = threading.Thread(target=web_command, args=[command_dictionary], daemon=True)
    user_command_thread.start()
    
    #waiting for hotword
    if detect_hotword(command_dictionary) is True:
        command_dictionary['command'] = 'placeholder'
        command_dictionary['command'] = speech_to_text()
        
    return command_dictionary['command']
    
def change_mode(command):
    global current_mode, devices_initialized
    
    if get_command('switch', command) is False:
        return False
    
    for mode, mode_object in modes.items():
        #get synonyms from command dictionary
        if get_command(mode, command):
            #get modes from database
            available_modes = get_user_modes()
            
            if available_modes is None:
                whizzy_speak('No available modes, please enable a mode')
                return True
            
            is_available = available_modes[mode]
            
            if current_mode is not None:
                #check if same as current mode
                if current_mode['keyword'] == mode_object['keyword']:
                    whizzy_speak(f'Already in {current_mode["keyword"]} mode')
                    return True
                
            #new mode is enabled
            if is_available is True:
                current_mode = mode_object
                set_mode_text(mode_object['keyword'])
                whizzy_speak(f'Switched to {mode_object["keyword"]}')
                
                #initialize devices when smart control is turned'No available modes, please enable a mode' on
                if mode == 'smart_controls' and devices_initialized is False:
                    initialize_devices()
                    devices_initialized = True
                    
            #new mode is disabled
            elif is_available is False:
                whizzy_speak(f'{mode_object["keyword"].capitalize()} is disabled')
                
            return True
        
    return False

def login():
    global current_mode, date, start_time, devices_initialized
    
    #get date and time of login
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    start_time = get_time()
    
    #start after authentication
    set_mode_text('Logged in')
    whizzy_speak('Logged in, welcome')
    
    #get modes from database
    available_modes = get_user_modes()
    
    if available_modes is None:
        whizzy_speak('No available modes, please enable a mode')
        set_mode_text('No available modes')
        current_mode = None
        return
    
    elif available_modes['smart_controls'] is True:
        current_mode = modes['smart_controls']
        
        #initializing devices in the classroom
        initialize_devices()
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
    global current_mode, new_login, devices_initialized
    
    #whizzy speaks
    whizzy_speak(get_response('exit'))
    
    #turn off devices
    turn_off_devices()
    logout_user()
    
    #get logout time and record log
    end_time = get_time()
    classroom_log(date, start_time, end_time)
    
    #reset values
    new_login = True
    current_mode = None 
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
        if current_mode is not None:
            print(f'\nCurrent mode: {current_mode["keyword"]}')
            
        #accepting triggger of input
        set_show_mic_state(True)
        
        command = get_user_command();
        
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
        elif 'current' and 'mode' in command and current_mode is not None:
            whizzy_speak(f'Currently I am in the {current_mode["keyword"]} mode')
                
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
