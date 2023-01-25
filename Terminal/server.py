import socket
import threading
import subprocess
from applications.web import blackboard

#static IP address and port
HOST = '192.168.0.101'
PORT = 65432

application_location = {
    'teams' : 'C:\\Users\\Pat\\AppData\\Local\\Microsoft\\Teams\\current\\Teams.exe',
}

application_instance = {
    'teams' : None,
    'blackboard' : None,
}

def server():
    global application_instance
    print('Trying to start connection ......')
    
    while True:    
        try: 
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((HOST, PORT))
                print("Server has started, waiting for client to connect")
                s.listen(5)
                connection, address = s.accept()

                with connection:
                    print(f'Connection established with address : {address}')
                    data = str(connection.recv(1024).decode('utf-8'))
                    command, jwt = data.split(',') # command,jwt
                    message = 'Application not found'
                    
                    if 'open' in command:
                        if 'blackboard learn' in command:
                            threading.Thread(target=blackboard, daemon=True, args=[jwt, application_instance]).start()
                            message = 'blackboard learn has been opened'

                        elif 'microsoft teams' in command:
                            application_instance['teams'] = subprocess.Popen([application_location['teams']])
                            message = 'microsoft teams has been opened'

                    elif 'close' in command:
                        if 'blackboard learn' in command:
                            if application_instance['blackboard'] is None:
                                message = 'blackboard learn is not open'
                            else:
                                application_instance['blackboard'].close()
                                message = 'blackboard has been closed'

                        elif 'microsoft teams' in command:
                            if application_instance['teams'] is None:
                                message = 'microsoft teams learn is not open'
                            else:
                                application_instance['teams'].kill()
                                application_instance['teams'] = None
                                message = 'microsoft teams has been closed'

                    connection.sendall(message.encode('utf-8'))
        except Exception as e:
            continue

if __name__ == '__main__':
    while True:
        server()