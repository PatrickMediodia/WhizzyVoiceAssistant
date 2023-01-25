import os
import base64 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

key = os.environ.get('AES_KEY').encode('utf-8') #16 char for AES128
iv = os.environ.get('AES_IV').encode('utf-8') #16 char for AES128, FIX IV

def decrypt(enc):
    enc = base64.b64decode(enc)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc),16)