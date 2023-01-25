import json
import requests

import base64 
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

#CBC with Fix IV
key = '+>UdZCdK.f7b!H+7' #16 char for AES128
iv =  'R7Rav`v){KUf:G{2'.encode('utf-8') #16 char for AES128, FIX IV

def decrypt(enc):
    enc = base64.b64decode(enc)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc),16)

url = "https://api.jhonlloydclarion.online/api/"

def get_bbl_account_credentials(jwt):
    end_point = url + 'users/me'
    end_point += '?populate=bbl'

    headers = {
        'Authorization': 'Bearer ' + jwt,
        'Content-Type': 'application/json'
    }

    #get account credentials
    response = requests.request("GET", end_point, headers=headers)
    response_json = json.loads(response.text)
    response_json = response_json['bbl']

    #decrypt pasword
    decrypted = decrypt(response_json['password'])
    response_json['password'] = decrypted.decode("utf-8", "ignore")

    return response_json
