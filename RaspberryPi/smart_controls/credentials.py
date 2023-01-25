import base64 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

key = '+>UdZCdK.f7b!H+7' #16 char for AES128
iv =  'R7Rav`v){KUf:G{2'.encode('utf-8') #16 char for AES128, FIX IV

def decrypt(enc):
    enc = base64.b64decode(enc)
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc),16)