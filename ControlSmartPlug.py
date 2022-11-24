from PyP100 import PyP100
import time

username = 'whizzyassistant@gmail.com'
password = 'Admin1234@'

# IP of Smart Plug, Account Credentials
p100 = PyP100.P100('192.168.1.9', username, password)

p100.handshake()
p100.login()


def device_state(): 
    print(p100.getDeviceInfo()['result']['device_on'])

def turnOnPlug():
    p100.turnOn()
    print('Turned On')
    
def turnOffPlug():
    p100.turnOff()
    print('Turned Off')



