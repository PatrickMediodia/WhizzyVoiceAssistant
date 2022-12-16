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

    headers = {
      'Content-Type': 'application/json'
    }
    
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

def get_lesson_data(jwt, trigger_word):
    end_point = url + 'users/me?'
    end_point += 'populate[0]=courses'
    end_point += '&populate[1]=courses.modules'
    end_point += '&populate[2]=courses.modules.lessons'
    end_point += '&populate[4]=courses.modules.lessons.trivias'
    end_point += '&populate[3]=courses.modules.lessons.questions'
    end_point += '&fields=id,username,email'
    
    headers = {
        'Authorization': 'Bearer ' + jwt
    }
    
    response = requests.request("GET", end_point, headers=headers)

    user_data_dict = json.loads(response.text)
    user_data_object = UserData(**user_data_dict)

    for course in user_data_object.courses:
        for module in course.modules:
            for lesson in module.lessons:
                if lesson.trigger_word is None:
                    continue
                if trigger_word in lesson.trigger_word:
                    print('Found trigger word')
                    return lesson
                
    return None

def detect_intent_texts(project_id, session_id, text, language_code):    
    session_client = dialogflow.SessionsClient()
    
    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    print("=" * 20)
    print("Query text: {}".format(response.query_result.query_text))
    print(
        "Detected intent: {} (confidence: {})\n".format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence,
        )
    )
    print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))
    
detect_intent_texts('whizzy-1d843', 'dasdasdasdsada3132131', 'Begin introduction', 'en')
