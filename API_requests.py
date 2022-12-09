import json
import requests
from models.account import Account
from models.userData import UserData

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

def get_lesson_data(jwt, trigger_word):
    url = 'https://api.jhonlloydclarion.online/api/users/me?populate[0]=courses&populate[1]=courses.modules&populate[2]=courses.modules.lessons&fields=id,username,email'

    headers = {
        'Authorization': 'Bearer ' + jwt
    }

    response = requests.request("GET", url, headers=headers, data={})

    user_data_dict = json.loads(response.text)
    user_data_object = UserData(**user_data_dict)

    for course in user_data_object.courses:
        for module in course.modules:
            for lesson in module.lessons:
                if trigger_word in lesson.trigger_word:
                    print('Found trigger word')
                    return lesson
                
    return None