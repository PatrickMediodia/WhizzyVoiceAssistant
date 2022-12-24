import json
from PyP100 import PyP100
#from text_to_speech import gtts_speak
from API_requests import get_jwt_token, get_room_device_data, set_device_status, authenticate #Remove authenticate

#TABO credentails
username = 'whizzyassistant@gmail.com'
password = 'Admin1234@'

#room details
room_number = 'R200'
room_device_data = None

#{id : PyP100 Object} relation
device_id_to_object_map = {}

def initialize_devices():
    global room_device_data
    global device_id_to_object_map

    print('Initializing devices ........')

    room_device_data = get_room_device_data(get_jwt_token(), room_number)

    for device in room_device_data:
        attributes = device['attributes']
        id = device['id']

        try:
            #check if id has PyP100 object in dictionary
            if device_id_to_object_map.get(id) == None:
                print('Initialize')
                initiated_device = PyP100.P100(attributes['ip_address'], username, password)
                initiated_device.handshake()
                initiated_device.login()
                device_id_to_object_map[id] = initiated_device

            #reflect the current state based on db
            if attributes['status'] == True:
                device_id_to_object_map[id].turnOn()
            else:
                device_id_to_object_map[id].turnOff()

            attributes['connected'] = True
            print(f'\n{attributes["name"]} is connected')
        except:
            attributes['connected'] = False
            print(f'\n{attributes["name"]} is not connected')

    print('\n', room_device_data)
    
def start_smart_controls(command):
    initialize_devices()

    for device in room_device_data:
        attributes = device['attributes']

        if attributes['name'] in command:
            if attributes['status'] == 'Not connected':
                #gtts_speak(f'{device_name} is not connected')
                print(f'{attributes["name"]} is not connected')
                break
            elif 'status' in command:
                device_status(device)
                break
            elif 'on' in command:
                turn_on_device(device)
                break
            elif 'off' in command:
                turn_off_device(device)
                break
    else:
        #gtts_speak('Command not found')
        print('Command not found')

def device_status(device_dict):
    attributes = device_dict['attributes']
    status = ''
    
    if get_device_state(attributes['object']) == True:
        set_device_status(device_dict['id'], 'true')
        status = 'on'
    elif get_device_state(attributes['object']) == False:
        set_device_status(device_dict['id'], 'false')
        status = 'off'
    #gtts_speak(f'{device_name} is currently {status}')
    print(f'{device_dict["name"]} is currently {status}')

def get_device_state(device):
    return device.getDeviceInfo()['result']['device_on']

def turn_on_device(device_dict):
    attributes = device_dict['attributes']

    if get_device_state(attributes['object']) == True:
        #gtts_speak(f'{device_name} is already on')
        print(f'{attributes["name"]} is already on')
        return

    attributes['object'].turnOn()
    set_device_status(device_dict['id'], 'true')

    #gtts_speak(f'{device_name} turned on')
    print(f'{attributes["name"]} turned on')

def turn_off_device(device_dict):
    global room_device_data
    attributes = device_dict['attributes']

    if get_device_state(attributes['object']) == False:
        #gtts_speak(f'{device_name} is already off')
        print(f'{attributes["name"]} is already off')
        return

    attributes['object'].turnOff()
    set_device_status(device_dict['id'], 'false')
    #gtts_speak(f'{device_name} turned off')
    print(f'{attributes["name"]} turned off')

#test
authenticate('faculty1', '123456')
initialize_devices()
while True:
    command = input('\nEnter a command: ')
    start_smart_controls(command)