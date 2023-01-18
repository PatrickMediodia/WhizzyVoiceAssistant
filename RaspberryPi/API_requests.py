import json
import requests
from models.account import Account
from models.userData import UserData

url = "https://api.jhonlloydclarion.online/api/"
jwt = None

def authenticate(username, password):
    global jwt
    
    end_point = url + 'auth/local'

    headers = { 'Content-Type': 'application/json' }
    
    payload = json.dumps({
      "identifier": username,
      "password": password
    })
    
    response = requests.request("POST", end_point, headers=headers, data=payload)
    
    try:
        account_dict = json.loads(response.text)
        account_object = Account(**account_dict)
        jwt = account_object.jwt    
        return account_object
    except:
        return None
    
def get_user_data(trigger_word):
    end_point = url + 'users/me?'
    end_point += 'populate[0]=courses'
    end_point += '&populate[1]=courses.modules'
    end_point += '&populate[2]=courses.modules.lessons'
    end_point += '&populate[4]=courses.modules.lessons.trivias'
    end_point += '&populate[3]=courses.modules.lessons.questions'
    end_point += '&fields=id,username,email'
    
    headers = { 'Authorization': 'Bearer ' + jwt }
    
    response = requests.request("GET", end_point, headers=headers)
    user_data_dict = json.loads(response.text)
    user_data_object = UserData(**user_data_dict)

    return user_data_object

def get_room_device_data(room_number):
    end_point = url + 'rooms?'
    end_point += 'populate=devices'
    end_point += f'&filters[name][$eq]={room_number}'
    
    headers = { 'Authorization': 'Bearer ' + jwt }
    
    response = requests.request("GET", end_point, headers=headers)
    room_device_data = json.loads(response.text)

    for data in room_device_data['data']:
        return data['attributes']['devices']['data']

    return None

def get_device_status(device_id):
    end_point = url + f'devices/{device_id}'

    headers = { 'Authorization': 'Bearer ' + jwt }

    response = requests.request("GET", end_point, headers=headers)
    device_status = json.loads(response.text)

    return device_status['data']

def set_device_status(device_id, status):
    if jwt == None:
        return 'Please authenticate'

    end_point = url + f'devices/{device_id}'

    headers = {
        'Authorization': 'Bearer ' + jwt,
        'Content-Type': 'application/json'
    }

    payload = json.dumps({ "data" : { "status" : status } })

    response = requests.request("PUT", end_point, headers=headers, data=payload)
    device_status_response = json.loads(response.text)

    return device_status_response['data']

def set_device_connectivity(device_id, connected):
    if jwt == None:
        return 'Please authenticate'

    end_point = url + f'devices/{device_id}'

    headers = {
        'Authorization': 'Bearer ' + jwt,
        'Content-Type': 'application/json'
    }

    payload = json.dumps({ "data" : { "connected" : connected } })

    response = requests.request("PUT", end_point, headers=headers, data=payload)
    device_status_response = json.loads(response.text)

    return device_status_response['data']

authenticate('faculty1', '123456');
print(get_user_data('linear'))