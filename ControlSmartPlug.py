from PyP100 import PyP100
import time

username = 'whizzyassistant@gmail.com'
password = 'Admin1234@'

p100 = PyP100.P100('192.168.1.9', username, password)

p100.handshake()
p100.login()

while True:
    p100.turnOn()
    print('Turned On')

    time.sleep(5)
    
    p100.turnOff()
    print('Turned Off')
    
    time.sleep(5)


