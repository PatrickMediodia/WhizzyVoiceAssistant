import json
import requests
from models.account import Account
from models.userData import UserData
from google.cloud import dialogflow

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