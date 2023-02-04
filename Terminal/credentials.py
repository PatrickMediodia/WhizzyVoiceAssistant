import os
import json
import base64
import requests
from Crypto.Cipher import AES
from dotenv import load_dotenv
from Crypto.Util.Padding import unpad

load_dotenv()

url = os.getenv('URL')
key = os.getenv('AES_KEY').encode('utf-8')
iv = os.getenv('AES_IV').encode('utf-8')

def decrypt(enc):
    enc = base64.b64decode(enc)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc),16)

def get_bbl_account_credentials(jwt, user_id, account_details):
    end_point = url + f'users/{user_id}'
    end_point += '?populate=bbl'

    headers = {
        'Authorization': 'Bearer ' + jwt,
        'Content-Type': 'application/json'
    }

    #get account credentials
    response = requests.request("GET", end_point, headers=headers)
    response_json = json.loads(response.text)
    
    #decrypt pasword
    decrypted = decrypt(response_json['bbl']['password'])

    #set account details
    account_details['email'] = response_json['bbl']['email']
    account_details['password'] = decrypted.decode("utf-8", "ignore")

def get_teams_account_credentials(jwt, user_id, account_details):
    end_point = url + f'users/{user_id}'
    end_point += '?populate=teams'

    headers = {
        'Authorization': 'Bearer ' + jwt,
        'Content-Type': 'application/json'
    }

    #get account credentials
    response = requests.request("GET", end_point, headers=headers)
    response_json = json.loads(response.text)
    
    #decrypt pasword
    decrypted = decrypt(response_json['teams']['password'])
    
    #set account details
    account_details['email'] = response_json['teams']['email']
    account_details['password'] = decrypted.decode("utf-8", "ignore")

