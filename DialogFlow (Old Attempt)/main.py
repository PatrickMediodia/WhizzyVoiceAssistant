import threading
from ALSA_handler import noalsaerr
from text_to_speech import gtts_speak
from speech_to_text import speech_to_text
from whizzy_avatar import initialize_avatar
from web_searching import start_google_assistant
from picovoice.detect_hotword import detect_hotword
from API_requests import authenticate, detect_intent
from google.protobuf.json_format import MessageToDict
from interactive_discussion import start_interactive_discussion
from smart_controls import initialize_devices, start_smart_controls

modes = (
    'web searching',
    'smart control',
    'interactive discussion'
)

mode_map = {
    'web searching': start_google_assistant,
    'smart control': start_smart_controls,
    'interactive discussion': start_interactive_discussion
}

#temporary credentials
username = "faculty1"
password = "123456"

#Session id must be unique to each raspberry PI
#Denotes the current conversation
session_id = 'RoomNumber'
project_id = 'whizzy-1d843'
response = None

current_mode = modes[1]

'''
def process_input():
    response_json = None
    hasResponse = False
    
    while True:
        command = speech_to_text()
        
        if command == '':
            return
        
        #get intent of comand
        response_object = detect_intent(project_id, session_id, command, 'en')
        response_json = MessageToDict(response_object._pb)
            
        print(response_json)
        
        try:
            for context in response_json['queryResult']['outputContexts']:
                print(f'Name: {context["name"]}')
                print(f'Life Span Count: {context["lifespanCount"]}')
                print(f'Parameters: {context["parameters"]}')
                
                #if context has dialog
                if 'dialog_context' in context["name"]:
                    #get dialog from json object
                    for text_object in response_json['queryResult']['fulfillmentMessages']:
                        for text in text_object['text']['text']:
                            if text != '':
                                gtts_speak(text)
                                break
        except:
            print('No output contexts')
            break
        
    return response_json
'''

def process_input():
    response_json = None
    hasResponse = False
    
    command = speech_to_text()
        
    if command == '':
        return
        
    #get intent of comand
    response_object = detect_intent(project_id, session_id, command, 'en')
    response_json = MessageToDict(response_object._pb)
            
    #print(response_json)
    
    #print output contexts
    try:
        for context in response_json['queryResult']['outputContexts']:
                #.split("/contexts/")[1]
            print(f'Context: {context["name"]}')
            print(f'Life Span Count: {context["lifespanCount"]}')
            #print(f'Parameters: {context["parameters"]}')
    except:
        print('No output contexts')

    
    #say fulfillment messages
    try:
        gtts_speak(response_object.query_result.fulfillment_messages[0].text.text[0])
    except:
        print('No fulfillment messages')

    return response_json

def change_mode(requested_mode):
    global current_mode
    
    if requested_mode == current_mode:
        gtts_speak(f'Already in {current_mode}')
        return
    
    for mode in modes:
        if requested_mode.lower() == mode and current_mode != mode:
            current_mode = mode
            gtts_speak(f'Switched to {mode}')
            break
    else:
        gtts_speak('Mode not found')
        
def main():
    global current_mode
    account = authenticate(username, password)
    
    if account == None:
        gtts_speak('Incorrect credentials')
        print('Incorrect credentials')
        return
    
    #start after authentication
    #initializing devices in the classroon
    initialize_devices()
    
    #start new thread for avatar
    '''
    threading.Thread(target=initialize_avatar).start()
    gtts_speak('Hello I am Whizzy, your personal assistant')
    '''
    
    with noalsaerr():
        while True:
            print(f'Current mode: {current_mode}')
            if detect_hotword():
                response = process_input()
                if response is not None:
                    #check if all parameters are complete
                    try:
                        response['queryResult']['allRequiredParamsPresent']
                    except:
                        print('Parameters are not complete')
                        continue
                    
                    action = response['queryResult']['action']
                    
                    #change mode
                    if action == 'ChangeMode':
                        change_mode(response['queryResult']['parameters']['Mode'])
                        
                    #current mode of Whizzy
                    elif action == 'CurrentMode':
                        gtts_speak(f"Currently I am in the {current_mode} mode")
                    
                    elif action == 'InteractiveDiscussion':
                        change_mode(modes[2])
                        
                    #send command to current mode
                    else:
                        mode_map[current_mode](response)
                        
if __name__ == '__main__':
    main()