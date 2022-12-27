import os
import socket
import signal
import webbrowser
import subprocess

HOST = '192.168.1.4'
PORT = 65432

application_map = {
    'application' : 'address in host computer',
    'MSTeams' : 'C:\\Users\\Pat\\AppData\\Local\\Microsoft\\Teams\\current\\Teams.exe',
}

MSTeamsProcess = None

def server():
    global MSTeamsProcess

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Server has started, waiting for client to connect")
        s.bind((HOST, PORT))
        s.listen(5)
        connection, address = s.accept()

        with connection:
            print(f'Connection established with address : {address}')

            while True:
                data = str(connection.recv(1024).decode('utf-8'))

                if 'open' in data:
                    if 'browser' in data:
                        print(f"Opening browser {data}")
                        webbrowser.open("www.google.com")                   
                        connection.sendall(f'{data} has been opened'.encode('utf-8'))

                    elif 'MSTeams' in data:
                        connection.sendall(f'{data} has been opened'.encode('utf-8'))
                        MSTeamsProcess = subprocess.Popen([application_map['MSTeams']])

                elif 'close' in data:
                    if 'MSTeams' in data:
                        print('trying to close MSTeams')
                        MSTeamsProcess.kill()
                        connection.sendall(f'{data} has been closed'.encode('utf-8'))

                else:
                    connection.sendall('Application not found'.encode('utf-8'))
                    break

if __name__ == '__main__':
    while True:
        server()