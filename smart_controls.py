import time
from PyP100 import PyP100
from text_to_speech import gtts_speak
from speech_to_text import speech_to_text

#TABO credentails
username = 'whizzyassistant@gmail.com'
password = 'Admin1234@'

#list of devices
devices = {
    'projector' : {
        'ip-address' : '192.168.1.10',
        'object' : None,
        'connected' : False,
    }
}

def initialize_devices():
    print('Initializing devices ........')

    for key, device in devices.items():
        try:
            initiated_device = PyP100.P100(
                                    device['ip-address'],
                                    username,
                                    password
                                )
            initiated_device.handshake()
            initiated_device.login()
            
            device['object'] = initiated_device
            device['connected'] = True
          
            print(f'\n{key} is connected\n')
        except:
            print(f'\n{key} is not connected\n')
        
def start_smart_controls(command):
    for device_name, device_dict in devices.items():
        device_object = device_dict['object']
        
        if key in command:
            if device_dict['connected'] == False:
                gtts_speak(f'{key} is not connected')
                break
            elif 'status' in command:
                device_status(device_name, device_object)
                break
            elif 'on' in command:
                turn_on_device(device_name, device_object)
                break
            elif 'off' in command:
                turn_off_device(device_name, device_object)
                break
    else:
        gtts_speak('Command not found')
        
def turn_on_device(device_name, device_object):
    if get_device_state(device_object) == True:
        gtts_speak(f'{device_name} is already on')
        return
    
    device_object.turnOn()
    gtts_speak(f'{device_name} turned on')

def turn_off_device(device_name, device_object):
    if get_device_state(device_object) == False:
        gtts_speak(f'{device_name} is already off')
        return
    
    device_object.turnOff()
    gtts_speak(f'{device_name} turned off')

def device_status(device_name, device_object):
    status = ''
    if get_device_state(device_object) == True:
        status = 'on'
    elif get_device_state(device_object) == False:
        status = 'off'
    gtts_speak(f'{device_name} is currently {status}')

def get_device_state(device): 
    return device.getDeviceInfo()['result']['device_on']