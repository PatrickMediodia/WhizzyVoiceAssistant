import socket
import webbrowser
import subprocess

HOST = '192.168.1.4'
PORT = 65432

application_map = {
    'microsoft teams' : 'C:\\Users\\Pat\\AppData\\Local\\Microsoft\\Teams\\current\\Teams.exe',
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
                        connection.sendall(f'browser has been opened'.encode('utf-8'))

                    elif 'microsoft teams' in data:
                        connection.sendall(f'microsoft teams has been opened'.encode('utf-8'))
                        MSTeamsProcess = subprocess.Popen([application_map['microsoft teams']])

                elif 'close' in data:
                    if 'microsoft teams' in data:
                        print('trying to close MSTeams')
                        MSTeamsProcess.kill()
                        connection.sendall(f'{data} has been closed'.encode('utf-8'))

                else:
                    connection.sendall('Application not found'.encode('utf-8'))
                    break
                
if __name__ == '__main__':
    while True:
        server()