import os
import json
import requests
from models.account import Account
from models.userData import UserData

room_number = os.environ.get('ROOM_NUMBER')
token = os.environ.get('BEARER_TOKEN')
url = os.environ.get('URL')

user_id = None
user_name = None
room_logged_in_id = None

def get_logged_in():
    global user_id, user_name, room_logged_in_id
    
    end_point = url + 'users?'
    end_point += 'populate=room_logged_in'
    end_point += f'&filters[room_logged_in][room][$eq]={room_number}'
    end_point += '&filters[room_logged_in][status][$eq]=True'
    
    headers = { 'Authorization': 'Bearer ' + token }
    
    response = requests.request("GET", end_point, headers=headers)
    logged_in_user = json.loads(response.text)
    
    #check if a user is logged in
    if len(logged_in_user) > 0:
        #store user id
        for user in logged_in_user:
            print(f'Logged in: {user["full_name"]}')
            user_id = user['id']
            user_name = user["full_name"]
            room_logged_in_id = user['room_logged_in']['id']
        return True
    
    return False

def logout_user():
    global user_id, room_logged_in_id
    
    end_point = url + f'users/{user_id}'
    
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
    
    payload = json.dumps({
        "room_logged_in" : {
            "id" : room_logged_in_id,
            "room": None,
            "status": False
            }
        })
    
    response = requests.request("PUT", end_point, headers=headers, data=payload)
    
    user_id = None
    room_logged_in_id = None

def get_user_id():
    return user_id

def get_user_data():
    end_point = url + f'users/{user_id}?'
    end_point += 'populate[0]=courses'
    end_point += '&populate[1]=courses.modules'
    end_point += '&populate[2]=courses.modules.lessons'
    end_point += '&populate[4]=courses.modules.lessons.trivias'
    end_point += '&populate[3]=courses.modules.lessons.questions'
    end_point += '&fields=id,username,email'
    
    headers = { 'Authorization': 'Bearer ' + token }
    
    response = requests.request("GET", end_point, headers=headers)
    user_data_dict = json.loads(response.text)
    user_data_object = UserData(**user_data_dict)

    return user_data_object

def get_room_device_data():
    end_point = url + 'rooms?'
    end_point += 'populate=devices'
    end_point += f'&filters[name][$eq]={room_number}'
    
    headers = { 'Authorization': 'Bearer ' + token }
    
    response = requests.request("GET", end_point, headers=headers)
    room_device_data = json.loads(response.text)
    
    try:
        for data in room_device_data['data']:
            return data['attributes']['devices']['data']
    except:
        return None
    
def get_device_status(device_id):
    end_point = url + f'devices/{device_id}'

    headers = { 'Authorization': 'Bearer ' + token }

    response = requests.request("GET", end_point, headers=headers)
    device_status = json.loads(response.text)

    return device_status['data']

def set_device_status(device_id, status):
    end_point = url + f'devices/{device_id}'

    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    payload = json.dumps({ "data" : { "status" : status } })

    response = requests.request("PUT", end_point, headers=headers, data=payload)
    device_status_response = json.loads(response.text)

    return device_status_response['data']

def set_device_connectivity(device_id, connected):
    end_point = url + f'devices/{device_id}'

    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    payload = json.dumps({ "data" : { "connected" : connected } })

    response = requests.request("PUT", end_point, headers=headers, data=payload)
    device_status_response = json.loads(response.text)

    return device_status_response['data']

def get_local_account_credentials():
    end_point = url + f'users/{user_id}'
    end_point += '?populate=local'
    
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", end_point, headers=headers)
    response_json = json.loads(response.text)
    
    return response_json['local']

def classroom_log(date, time_in, time_out):
    end_point = url + 'logs'
    
    payload = json.dumps({
      "data": {
        "name": user_name,
        "room": room_number,
        "date": date,
        "time_in": time_in,
        "time_out": time_out
      }
    })
    
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", end_point, headers=headers, data=payload)
    print(response, date, time_in, time_out)

url = 'https://api.jhonlloydclarion.online/api/'
token = 'c4e2d7ae80175496dd9ed92feb2433c52050cf995c7ee17d513fb7c6f60aea3ab18019f7f772c3f47f26482c00e73ba54e4f1f15bc5e705bd1c36e543daea8b7327c215b70ea0e105f060e4e8e2e5e69a61dc89ab7cce1a643c8fbc2be2bbf66d51ede4b4d670b3bce2f4ac4e165c8bcf613ce7bfa2548c8cb5a8b187f4f42ae'
user_id = 1

def get_user_modes():
    end_point = url + f'users/{user_id}?populate[0]=modes'
    
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.request("GET", end_point, headers=headers)
        response_json = json.loads(response.text)
        return response_json['modes']
    
    except:
        return None