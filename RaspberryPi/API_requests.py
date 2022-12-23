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
    
def get_jwt_token():
    if jwt is None:
        print('No jwt token, please authenticate')
        return
    return jwt
    
def get_user_data(jwt, trigger_word):
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
        
class Room:
    def __init__(self, id, attributes):
        self.id = id
        self.attributes = RoomAttributes(**attributes)
    	
class RoomAttributes:
    def __init__(self, createdAt, updatedAt, publishedAt, name, devices):
        self.createdAt = createdAt,
        self.updatedAt = updatedAt,
        self.publishedAt = publishedAt,
        self.name = name
        self.devices = [ Device(**device) for device in devices['data'] ]
    
class Device:
    def __init__(self, id, attributes):
        self.id = id
        self.attributes = DeviceAttributes(**attributes)

class DeviceAttributes:
    def __init__(self, name, identifier, status, createdAt, updatedAt, publishedAt):
        self.name = name
        self.identifier = identifier
        self.status = status
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.publishedAt = publishedAt
	
def get_room_device_data(jwt, room_number):
    end_point = url + 'rooms?'
    end_point += 'populate=devices'
    end_point += f'&filters[name][$eq]={room_number}'
    
    headers = { 'Authorization': 'Bearer ' + jwt }
    
    response = requests.request("GET", end_point, headers=headers)
    
    print(response.text)

    room_device_data = json.loads(response.text)

    print(room_device_data)

get_room_device_data('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiaWF0IjoxNjcxNzc1MTk4LCJleHAiOjE2NzQzNjcxOTh9.HPLFNXzrAJXi8Zcg9Kyepg5Fl9xk0SPQQeuroNZF-_c', 'R200')    
