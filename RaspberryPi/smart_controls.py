import time
from PyP100 import PyP100
#from text_to_speech import gtts_speak
from API_requests import get_jwt_token, get_room_device_data, set_device_status, authenticate #Remove authenticate

#TABO credentails
username = 'whizzyassistant@gmail.com'
password = 'Admin1234@'

#room details
room_number = 'R200'

#list of devices
devices = {
    'R200-projector' : {
        'id' : None,
        'name' : 'projector',
        'object' : None,
        'ip-address' : '192.168.1.10',
        'status' : 'Not connected',
    },
    'R200-computer' : {
        'id' : None,
        'name' : 'computer',
        'object' : None,
        'ip-address' : '192.168.1.11',
        'status' : 'Not connected',
    },
    'R200-light-1' : {
        'id' : None,
        'name' : 'light',
        'object' : None,
        'ip-address' : '192.168.1.13',
        'status' : 'Not connected',  
    }
}

def initialize_device(key, device, room_device_data):
    try:
        #set device id
        for device_data in room_device_data:
            if device_data['attributes']['identifier'] == key:
                device['id'] = device_data['id']
                break
        
        #initiate device object
        initiated_device = PyP100.P100(device['ip-address'], username, password)
        initiated_device.handshake()
        initiated_device.login()

        device['object'] = initiated_device
        device['status'] = get_device_state(initiated_device)

        print(f'\n{key} is connected')
    except:
        print(f'\n{key} is not connected')

def initialize_devices():
    print('Initializing devices ........')

    room_device_data = get_room_device_data(get_jwt_token(), room_number)

    for key, device in devices.items():
        initialize_device(key, device, room_device_data)

    print(devices)

def start_smart_controls(command):
    for key, device_dict in devices.items():
        if device_dict['name'] in command:
            if device_dict['status'] == 'Not connected':
                #gtts_speak(f'{device_name} is not connected')
                print(f'{device_dict["name"]} is not connected')
                break
            elif 'status' in command:
                device_status(device_dict)
                break
            elif 'on' in command:
                turn_on_device(device_dict)
                break
            elif 'off' in command:
                turn_off_device(device_dict)
                break
    else:
        #gtts_speak('Command not found')
        print('Command not found')
        
def turn_on_device(device_dict):
    if get_device_state(device_dict['object']) == True:
        #gtts_speak(f'{device_name} is already on')
        print(f'{device_dict["name"]} is already on')
        return

    device_dict['object'].turnOn()
    set_device_status(device_dict['id'], 'true')

    #gtts_speak(f'{device_name} turned on')
    print(f'{device_dict["name"]} turned on')

def turn_off_device(device_dict):
    if get_device_state(device_dict['object']) == False:
        #gtts_speak(f'{device_name} is already off')
        print(f'{device_dict["name"]} is already off')
        return

    device_dict['object'].turnOff()
    set_device_status(device_dict['id'], 'false')
    #gtts_speak(f'{device_name} turned off')
    print(f'{device_dict["name"]} turned off')

def device_status(device_dict):
    status = ''
    if get_device_state(device_dict['object']) == True:
        set_device_status(device_dict['id'], 'true')
        status = 'on'
    elif get_device_state(device_dict['object']) == False:
        set_device_status(device_dict['id'], 'true')
        status = 'off'
    #gtts_speak(f'{device_name} is currently {status}')
    print(f'{device_dict["name"]} is currently {status}')

def get_device_state(device):
    return device.getDeviceInfo()['result']['device_on']

#test
authenticate('faculty1', '123456')
initialize_devices()
while True:
    command = input('\nEnter a command: ')
    start_smart_controls(command)