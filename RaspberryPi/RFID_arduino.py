'''
pip install pyserial
'''

import serial

serialObj = serial.Serial(
    'COM5',
    9600,
    timeout=1
)

#dummy data
def authenticate_RFID(rfid_UID):
    teacher_RFID = {
        #userID : RFID tag relation
        'Dennis Martiliano' : '9324519',
        'Patrick Mediodia' : '8EB0723F',
    }

    for teacher, UID in teacher_RFID.items():
        if UID == rfid_UID:          
            return True
    else:
        return False

while True:
    msg = serialObj.readline()
    rfid_UID = msg.decode('utf-8').strip()

    if rfid_UID != '':
        result = authenticate_RFID(rfid_UID)

        if result:
            print(f'Access granted, {rfid_UID}')
            serialObj.write(b'Granted\n')
        else:
            print(f'Access Denied, {rfid_UID}')
            serialObj.write(b'Denied\n')
    
        input("Press enter to be able to read another card: ")
        print('message sent')
        serialObj.write(b'Logout\n')