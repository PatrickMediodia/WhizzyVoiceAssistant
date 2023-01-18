import socket

#match details with server
HOST = '192.168.1.7'
PORT = 65432

application_map = {
    'microsoft teams' : ['microsoft teams', 'ms teams', 'teams'],
    'blackboard learn' : ['blackboard learn', 'blackboard', 'bbl'],
    'browser' : ['browser', 'web', 'web browser'],
}

def client(application):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            #connect to server
            s.settimeout(1)
            s.connect((HOST, PORT))
            
            #send message
            message = application.encode('utf-8')
            s.sendall(message)
            
            #receive response
            response = s.recv(1024).decode('utf-8')
            s.close()
            
            return response
            
        except Exception as e:
            print(e)
            return 'Cannot connect to host machine'