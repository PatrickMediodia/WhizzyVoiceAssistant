import json
import requests
from models.account import Account

url = "https://api.jhonlloydclarion.online/api/"

def authenticate(username, password):
    payload = json.dumps({
      "identifier": username,
      "password": password
    })
    
    headers = {
      'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url + 'auth/local', headers=headers, data=payload)
    
    try:
        account_dict = json.loads(response.text)
        account_object = Account(**account_dict)
        return account_object
    except:
        return

def get_module_data(token):
    headers = {
      'Authorization': 'Bearer ' + token
    }

    response = requests.request("GET", url + 'users/me?populate=deep', headers=headers)
    
    #parse json to object
    print(response.text)