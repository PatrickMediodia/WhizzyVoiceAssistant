import os
import socket
from API_requests import get_jwt

#match details with server
HOST = os.environ.get('HOST')
PORT = int(os.environ.get('PORT'))

application_map = {
    'microsoft teams' : ['microsoft teams', 'ms teams', 'teams'],
    'blackboard learn' : ['blackboard learn', 'blackboard', 'bbl'],
    'browser' : ['browser', 'web', 'web browser'],
}

def client(application):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            #connect to server
            #s.settimeout(1)
            s.connect((HOST, PORT))
            
            #send message
            #message,jwt format
            application += f',{get_jwt()}'
            message = application.encode('utf-8')
            s.sendall(message)
            
            #receive response
            response = s.recv(1024).decode('utf-8')
            s.close()
            
            return response
            
        except Exception as e:
            print(e)
            return 'Cannot connect to host machine'