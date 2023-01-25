import time
import socket
import webbrowser
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
                    found = False
                    print(f'Connection established with address : {address}')

                    data = str(connection.recv(1024).decode('utf-8'))
                    command, jwt = data.split(',') # command,jwt

                    if 'open' in command:
                        if 'browser' in command:
                            webbrowser.open("www.google.com")                   
                            connection.sendall(f'browser has been opened'.encode('utf-8'))
                            found = True

                        elif 'blackboard learn' in command:
                            connection.sendall(f'blackboard learn has been opened'.encode('utf-8'))
                            application_instance['blackboard'] = blackboard(jwt)
                            found = True

                        elif 'microsoft teams' in command:
                            connection.sendall(f'microsoft teams has been opened'.encode('utf-8'))
                            application_instance['teams'] = subprocess.Popen([application_location['teams']])
                            found = True
                            
                    elif 'close' in command:
                        if 'blackboard learn' in command:
                            if application_instance['blackboard'] is None:
                                connection.sendall(f'blackboard learn is not open'.encode('utf-8'))
                            else:
                                application_instance['blackboard'].close()
                                connection.sendall(f'blackboard has been closed'.encode('utf-8'))
                            found = True
                        elif 'microsoft teams' in command:
                            if application_instance['teams'] is None:
                                connection.sendall(f'microsoft teams is not open'.encode('utf-8'))
                            else:
                                application_instance['teams'].kill()
                                application_instance['teams'] = None
                                connection.sendall(f'microsoft teams has been closed'.encode('utf-8'))
                            found = True

                    if not found:
                        connection.sendall('Application not found'.encode('utf-8'))

        except Exception as e:
            pass

if __name__ == '__main__':
    while True:
        server()