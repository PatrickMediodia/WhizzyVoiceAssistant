import socket
import webbrowser
import subprocess
from applications.web import blackboard

#static IP address and port
HOST = '192.168.1.7'
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

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Server has started, waiting for client to connect")
        s.bind((HOST, PORT))
        s.listen(5)
        connection, address = s.accept()

        with connection:
            found = False
            print(f'Connection established with address : {address}')

            data = str(connection.recv(1024).decode('utf-8'))

            if 'open' in data:
                if 'browser' in data:
                    webbrowser.open("www.google.com")                   
                    connection.sendall(f'browser has been opened'.encode('utf-8'))
                    found = True

                elif 'blackboard learn' in data:
                    connection.sendall(f'blackboard learn has been opened'.encode('utf-8'))
                    application_instance['blackboard'] = blackboard('2019165202', 'changepassword1234')
                    found = True

                elif 'microsoft teams' in data:
                    connection.sendall(f'microsoft teams has been opened'.encode('utf-8'))
                    application_instance['teams'] = subprocess.Popen([application_location['teams']])
                    found = True
                    
            elif 'close' in data:
                if 'blackboard learn' in data:
                    if application_instance['blackboard'] is None:
                        connection.sendall(f'blackboard learn is not open'.encode('utf-8'))
                    else:
                        application_instance['blackboard'].close()
                        connection.sendall(f'blackboard has been closed'.encode('utf-8'))
                    found = True
                elif 'microsoft teams' in data:
                    if application_instance['teams'] is None:
                        connection.sendall(f'microsoft teams is not open'.encode('utf-8'))
                    else:
                        application_instance['teams'].kill()
                        application_instance['teams'] = None
                        connection.sendall(f'microsoft teams has been closed'.encode('utf-8'))
                    found = True

            if not found:
                connection.sendall('Application not found'.encode('utf-8'))

if __name__ == '__main__':
    while True:
        server()