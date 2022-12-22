try:
    import socket
    import threading
    import time
except:
    print('library not found ')

#match details with server
HOST = '192.168.1.4'
PORT = 65432

def client(application):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #connect to server
        s.connect((HOST, PORT))
        
        #send message
        message = application.encode('utf-8')
        s.sendall(message)
        
        #receive response
        response = s.recv(1024).decode('utf-8')
        print(f'Response : {response}')

        s.close()
        
client('open MSTeams')