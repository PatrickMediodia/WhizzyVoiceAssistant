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

#FLAG variable
startup = True

def initialize_devices():
    global startup
    global room_device_data
    global device_id_to_object_map
    
    while True:
        #refresh data every second
        time.sleep(1)

        #API call
        room_device_data = get_room_device_data(room_number)
        
        if room_device_data is None:
            print('Room device data cannot be fetched.')
            continue
        
        #iterate through devices
        for device in room_device_data:
            #deserialize json data
            attributes = device['attributes']
            id = device['id']

            try:
                #check if id has PyP100 object in dictionary
                if device_id_to_object_map.get(id) is None:
                    initiated_device = PyP100.P100(attributes['ip_address'], username, password)
                    initiated_device.handshake()
                    initiated_device.login()
                    device_id_to_object_map[id] = initiated_device
                    
                #set to connected
                if not attributes['connected']:
                    set_device_connectivity(id, True)
                    attributes['connected'] = True
                
                #turn PC on at startup
                if startup and attributes['name'] == 'computer':
                    pass
                    '''
                    startup = False #ignore on next iteration
                    print('Triggered on startup')
                    threading.Thread(target=open_terminal, daemon=True, args=[id]).start()
                    continue
                    '''
                    
                #reflect the current state based on db
                if attributes['status']:
                    device_id_to_object_map[id].turnOn()
                else:
                    device_id_to_object_map[id].turnOff()
                
            except:
                if attributes['connected']:
                    set_device_connectivity(id, False)
                    attributes['connected'] = False
                    device_id_to_object_map[id] = None
                    
def device_status(device_dict):
    attributes = device_dict['attributes']
    status = ''
    
    if attributes['status'] == True:
        status = 'on'
    elif attributes['status'] == False:
        status = 'off'
        
    whizzy_speak(f'{attributes["name"]} is currently {status}')

def turn_on_device(device_dict):
    attributes = device_dict['attributes']

    if attributes['status'] == True:
        whizzy_speak(f'{attributes["name"]} is already on')
        return
    
    elif attributes['name'] == 'computer':
        threading.Thread(target=open_terminal, daemon=True, args=[device_dict['id']]).start()
        return
    
    set_device_status(device_dict['id'], 'true')
    whizzy_speak(f'{attributes["name"]} turned on')

def turn_off_device(device_dict):
    attributes = device_dict['attributes']

    if attributes['status'] == False:
        whizzy_speak(f'{attributes["name"]} is already off')
        return
    
    elif attributes['name'] == 'computer':
        threading.Thread(target=close_terminal, daemon=True, args=[device_dict['id']]).start()
        return
    
    set_device_status(device_dict['id'], 'false')
    whizzy_speak(f'{attributes["name"]} turned off')

def open_terminal(id):
    set_device_status(id, 'true')
    whizzy_speak(f'Computer turned on')
    
    #get data from API
    account_credentials = get_local_account_credentials()
    
    #use decrypt function
    decrypted_password = decrypt(account_credentials['password'])
    
    #login to windows
    login_terminal(account_credentials['email'], decrypted_password.decode("utf-8", "ignore"))
    
def close_terminal(id):
    shutdown_terminal()
    whizzy_speak(f'Computer turned off')
    
    #wait until computer shutsdown
    while(check_terminal_status()):
        pass
    time.sleep(1)
    
    #set status to false
    set_device_status(id, 'false') 
    
def start_smart_controls(command):
    #check command for controlling devices
    for device in room_device_data:
        attributes = device['attributes']

        if attributes['name'] in command:
            if attributes['connected'] == False:
                whizzy_speak(f'{attributes["name"]} is not connected')
                return
            elif 'status' in command:
                device_status(device)
                return
            elif 'on' in command:
                turn_on_device(device)
                return
            elif 'off' in command:
                turn_off_device(device)
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