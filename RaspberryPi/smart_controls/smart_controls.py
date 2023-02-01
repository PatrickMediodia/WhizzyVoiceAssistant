import os
import time
import threading
from PyP100 import PyP100
from whizzy_avatar import whizzy_speak
from smart_controls.credentials import decrypt
from text_to_speech import get_response
from smart_controls.windows_script import login_terminal
from smart_controls.client import client, application_map
from smart_controls.windows_script import shutdown_terminal, check_terminal_status
from API_requests import get_room_device_data, set_device_status, set_device_connectivity, get_local_account_credentials

#TABO credentails
username = os.environ.get('TABO_USERNAME')
password = os.environ.get('TABO_PASSWORD')

#room details
room_number = os.environ.get('ROOM_NUMBER')
room_device_data = None

#{id : PyP100 Object} relation
device_id_to_object_map = {}

def initialize_devices():
    global room_device_data
    room_device_data = get_room_device_data(room_number)
        
    if room_device_data is None:
        print('Room device data cannot be fetched.')
        return
    
    for device_data in room_device_data:    
        initialize_device(device_data)
        
    print(room_device_data)
    print(device_id_to_object_map)
    
def initialize_device(device_data):
    global device_id_to_object_map
    
    print(f'Initializing {attributes["name"]}')
    attributes = device_data['attributes']
    id = device_data['id']
    
    try:
        initiated_device = PyP100.P100(attributes['ip_address'], username, password)
        initiated_device.handshake()
        initiated_device.login()
        device_id_to_object_map[id] = initiated_device
            
        set_device_connectivity(id, True)
        attributes['connected'] = True
            
        #reflect the current state based on db
        if attributes['status']:
            device_id_to_object_map[id].turnOn()
        else:
            device_id_to_object_map[id].turnOff()
                
    except:
        set_device_connectivity(id, False)
        attributes['connected'] = False
        device_id_to_object_map[id] = None
        
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
    room_device_data = get_room_device_data(room_number)

def get_device_status(id, name):
    global device_id_to_object_map
    
    #check if already in object map
    if device_id_to_object_map.get(id) is None:
        whizzy_speak(f'{name} is not connected')
        return None
    
    #try to get device status
    try:
        return device_id_to_object_map[id].getDeviceInfo()['result']['device_on']
    except:
        set_device_connectivity(id, False)
        device_id_to_object_map[id] = None
        whizzy_speak(f'{name} is not connected')
        return None
    
def device_status(device_dict):
    attributes = device_dict['attributes']
    id = device_dict['id']
    
    device_status = get_device_status(id, attributes["name"])
    if device_status is True:
        whizzy_speak(f'{attributes["name"]} is currently on')
    elif device_status is False:
        whizzy_speak(f'{attributes["name"]} is currently off')
        
def turn_on_device(device_dict):
    attributes = device_dict['attributes']
    id = device_dict['id']
    
    device_status = get_device_status(id, attributes["name"])
    if device_status is True:
        whizzy_speak(f'{attributes["name"]} is already on')
        return
    elif device_status is False:
        set_device_status(device_dict['id'], 'true')
        device_id_to_object_map[id].turnOn()
        whizzy_speak(f'{attributes["name"]} turned on')
    
def turn_off_device(device_dict): 
    attributes = device_dict['attributes']
    id = device_dict['id']
    
    device_status = get_device_status(id, attributes["name"])
    if device_status is False:
        whizzy_speak(f'{attributes["name"]} is already off')
        return
    elif device_status is True:
        set_device_status(device_dict['id'], 'false')
        device_id_to_object_map[id].turnOff()
        whizzy_speak(f'{attributes["name"]} turned off')
        
def start_smart_controls(command):
    refresh_room_device_data()
    
    #check command for controlling devices
    for device_data in room_device_data:
        attributes = device_data['attributes']
        if attributes['name'] in command:
            if attributes['connected'] == False:
                retry_initializing_device(attributes['name'], device_data)
                return
            if 'status' in command:
                device_status(device_data)
                return
            elif 'on' in command:
                turn_on_device(device_data)
                return
            elif 'off' in command:
                turn_off_device(device_data)
                return
    
    #check command for opening/closing applications
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