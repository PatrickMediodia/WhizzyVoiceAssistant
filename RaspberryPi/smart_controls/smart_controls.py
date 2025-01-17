import os
import time
import threading
from PyP100 import PyP100
from text_to_speech import get_response
from smart_controls.credentials import decrypt
from speech_to_text import get_command, replace_command
from smart_controls.client import client, application_map
from whizzy_avatar import whizzy_speak, set_show_mic_state
from smart_controls.windows_script import login_terminal, shutdown_terminal
from API_requests import get_room_device_data, set_device_status, set_device_connectivity, get_local_account_credentials

#TABO credentails
username = os.environ.get('TABO_USERNAME')
password = os.environ.get('TABO_PASSWORD')

#room details
room_device_data = None

#{id : PyP100 Object} relation
device_id_to_object_map = {}

def initialize_devices():
    global room_device_data
    room_device_data = get_room_device_data()
    
    print('\nInitializing devices ......\n')
    
    if room_device_data is None:
        print('Room device data cannot be fetched.')
        return
    
    for device_data in room_device_data:    
        initialize_device(device_data)
        
    print(device_id_to_object_map)
    
def initialize_device(device_data):
    global device_id_to_object_map
    
    attributes = device_data['attributes']
    id = device_data['id']
    print(f'Initializing {attributes["name"]}')

    try:
        initiated_device = PyP100.P100(attributes['ip_address'], username, password)
        initiated_device.handshake()
        initiated_device.login()
        device_id_to_object_map[id] = initiated_device
            
        set_device_connectivity(id, True)
        attributes['connected'] = True
    
        #turn PC on at startup
        if attributes['name'] == 'Computer':
            turn_on_pc_thread = threading.Thread(target=open_terminal, daemon=True, args=[id])
            turn_on_pc_thread.name = 'Turn on PC'
            turn_on_pc_thread.start()
            return
        
        #turn on light at startup
        if attributes['name'] == 'Light':
            device_id_to_object_map[id].turnOn()
            set_device_status(id, True)
            return
        
        #reflect the current state based on db
        if attributes['status']:
            device_id_to_object_map[id].turnOn()
        else:
            device_id_to_object_map[id].turnOff()
                
    except:
        set_device_connectivity(id, False)
        attributes['connected'] = False
        device_id_to_object_map[id] = None

def turn_off_devices():
    global device_id_to_object_map
    
    refresh_room_device_data()
    
    for device_dict in room_device_data:
        attributes = device_dict['attributes']
        id = device_dict['id']
        
        device_status = get_device_status(id, attributes["name"])
        
        if attributes['name'] == 'Computer' and device_status == True:
            close_terminal(id)
            
        elif device_status == True:
            set_device_status(device_dict['id'], False)
            device_id_to_object_map[id].turnOff()
            
def retry_initializing_device(thread_name, device_data):
    running_threads = threading.enumerate()
    
    #check if thread for initialization is already started
    for thread in running_threads:
        if thread.name == thread_name:
            print(f'Already trying to initialize {thread_name}')
            break
    else:
        new_thread = threading.Thread(target=initialize_device, args=[device_data], daemon=True)
        new_thread.name = thread_name
        new_thread.start()
        
    whizzy_speak(f'{thread_name} is not connected')
    
def refresh_room_device_data():
    global room_device_data
    room_device_data = get_room_device_data()
    
def get_device_status(id, name):
    global device_id_to_object_map
    
    #check if already in object map
    if device_id_to_object_map.get(id) is None:
        return None
    
    #try to get device status, changed timeout in PyP100 library (3 seconds)
    try:
        return device_id_to_object_map[id].getDeviceInfo()['result']['device_on']
    except:
        set_device_connectivity(id, False)
        device_id_to_object_map[id] = None
        return None
    
def device_status(device_dict):
    attributes = device_dict['attributes']
    id = device_dict['id']
    
    device_status = get_device_status(id, attributes["name"])
    
    if device_status is True:
        whizzy_speak(f'{attributes["name"]} is currently on')
        
    elif device_status is False:
        whizzy_speak(f'{attributes["name"]} is currently off')
        
    else:
        whizzy_speak(f'{name} is not connected')
        
def turn_on_device(device_dict):
    attributes = device_dict['attributes']
    id = device_dict['id']
    
    device_status = get_device_status(id, attributes["name"])
    
    if device_status is True:
        whizzy_speak(f'{attributes["name"]} is already on')

    #turn PC on at startup
    elif attributes['name'] == 'Computer':
        turn_on_pc_thread = threading.Thread(target=open_terminal, daemon=True, args=[id])
        turn_on_pc_thread.name = 'Turn on PC'
        turn_on_pc_thread.start()
        return
    
    elif device_status is False:
        set_device_status(device_dict['id'], True)
        device_id_to_object_map[id].turnOn()
        whizzy_speak(f'{attributes["name"]} turned on')
    
    else:
        whizzy_speak(f'{name} is not connected')
         
def turn_off_device(device_dict): 
    attributes = device_dict['attributes']
    id = device_dict['id']
    
    device_status = get_device_status(id, attributes["name"])
    
    if device_status is False:
        whizzy_speak(f'{attributes["name"]} is already off')
        
    elif attributes['name'] == 'Computer':
        turn_off_pc_thread = threading.Thread(target=close_terminal, daemon=True, args=[id])
        turn_off_pc_thread.name = 'Turn off PC'
        turn_off_pc_thread.start()
        return
    
    elif device_status is True:
        set_device_status(device_dict['id'], False)
        device_id_to_object_map[id].turnOff()
        whizzy_speak(f'{attributes["name"]} turned off')
    
    else:
        whizzy_speak(f'{name} is not connected')

def open_terminal(id):
    print('Triggered on computer')
    whizzy_speak(f'Computer turned on')
    
    set_device_status(id, True)
    device_id_to_object_map[id].turnOn()
    
    #get data from API
    account_credentials = get_local_account_credentials()
    
    if account_credentials is None:
        whizzy_speak(f'No computer credentials provided')
        print('\nNo computer credentials provided\n')
        return
    
    if account_credentials['password'] is None or account_credentials['email'] is None:
        whizzy_speak(f'Invalid computer credentials provided')
        print('\nInvalid computer credentials provided\n')
        return
    
    #use decrypt function
    decrypted_password = decrypt(account_credentials['password']).decode("utf-8", "ignore")
    
    #login to windows
    print('\nTrying to connect to terminal ......\n')
    while(login_terminal(account_credentials['email'], decrypted_password) is False):
        pass
    
def close_terminal(id):
    print('\nTrying to shutdown terminal ......\n')
    while(shutdown_terminal() is False):
        pass
    
    whizzy_speak(f'Computer turned off')
    set_show_mic_state(True)
    
    #set status to false
    set_device_status(id, False)
    device_id_to_object_map[id].turnOff()
    
def start_smart_controls(command):
    refresh_room_device_data()
    
    #account for room_device_data availability   
    try:
        #check command for controlling devices
        for device_data in room_device_data:
            attributes = device_data['attributes']
            
            if attributes['name'].lower() in command:
                if attributes['connected'] == False:
                    retry_initializing_device(attributes['name'], device_data)
                    return
                if 'status' in command:
                    device_status(device_data)
                    return
                elif get_command('on', command):
                    turn_on_device(device_data)
                    return
                elif get_command('off', command):
                    turn_off_device(device_data)
                    return
    except Exception as e:
        print(e)
        whizzy_speak(f'Room device data cannot be fetched')
    
    #check command for opening/closing applications  
    if get_command('open', command) or get_command('close', command):
        #check for synonyms
        command = replace_command('open', command)
        command = replace_command('close', command)
        
        for application, synonyms in application_map.items():
            for synonym in synonyms:
                if synonym in command:
                    #replace synonym with something the receiver can understand
                    request_to_send = command.replace(synonym, application)
                        
                    #resend request and get response
                    server_response = client(request_to_send)
                    whizzy_speak(server_response)
                        
                    return
                
    #script will return to main if keyword found
    #speak if not returned
    whizzy_speak(get_response('notFound'))
