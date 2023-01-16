import time
from PyP100 import PyP100
from text_to_speech import gtts_speak
from smart_controls.client import client, application_map
from API_requests import get_room_device_data, set_device_status, set_device_connectivity

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

    while True:
        #refresh data every second
        time.sleep(1)

        #API call
        room_device_data = get_room_device_data(room_number)
        
        #iterate through devices
        for device in room_device_data:
            #deserialize json data
            attributes = device['attributes']
            id = device['id']

            try:
                #check if id has PyP100 object in dictionary
                if device_id_to_object_map.get(id) == None:
                    initiated_device = PyP100.P100(attributes['ip_address'], username, password)
                    initiated_device.handshake()
                    initiated_device.login()
                    device_id_to_object_map[id] = initiated_device

                #reflect the current state based on db
                if attributes['status'] == True:
                    device_id_to_object_map[id].turnOn()
                else:
                    device_id_to_object_map[id].turnOff()

                set_device_connectivity(id, True)
                attributes['connected'] = True

            except:
                set_device_connectivity(id, False)
                attributes['connected'] = False
                
def device_status(device_dict):
    attributes = device_dict['attributes']
    status = ''
    
    if attributes['status'] == True:
        status = 'on'
    elif attributes['status'] == False:
        status = 'off'
        
    gtts_speak(f'{attributes["name"]} is currently {status}')

def turn_on_device(device_dict):
    attributes = device_dict['attributes']

    if attributes['status'] == True:
        gtts_speak(f'{attributes["name"]} is already on')
        return

    set_device_status(device_dict['id'], 'true')
    gtts_speak(f'{attributes["name"]} turned on')

def turn_off_device(device_dict):
    attributes = device_dict['attributes']

    if attributes['status'] == False:
        gtts_speak(f'{attributes["name"]} is already off')
        return

    set_device_status(device_dict['id'], 'false')
    gtts_speak(f'{attributes["name"]} turned off')

def start_smart_controls(command):
    #check command for controlling devices
    for device in room_device_data:
        attributes = device['attributes']

        if attributes['name'] in command:
            if attributes['connected'] == False:
                gtts_speak(f'{attributes["name"]} is not connected')
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
                gtts_speak(server_response)
                
                return
            
    #script will return to main if keyword found
    #speak if not returned
    gtts_speak('Command not found')