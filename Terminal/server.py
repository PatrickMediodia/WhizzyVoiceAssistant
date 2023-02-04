'''
Add server.py to shell:common per user
This is so that the server.py script will only open on per login of user
'''

import os
import socket
import threading
import subprocess
from dotenv import load_dotenv
from msteams.teams import open_teams
from blackboard import open_blackboard

load_dotenv()

#static IP address and port
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))

application_instance = {
    'teams' : None,
    'blackboard' : None,
}

def server():
    global application_instance
    
    try: 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            print("Server has started, waiting for client to connect")
            s.listen(5)
            connection, address = s.accept()

            with connection:
                print(f'Connection established with address : {address}')
                data = str(connection.recv(1024).decode('utf-8'))
                command, token, user_id = data.split(',') # command,token,user_id
                message = 'Application not found'
                    
                if 'open' in command:
                    if 'blackboard learn' in command:
                        threading.Thread(target=open_blackboard, daemon=True, args=[token, user_id, application_instance]).start()
                        message = 'blackboard learn has been opened'

                    elif 'microsoft teams' in command:
                        threading.Thread(target=open_teams, daemon=True, args=[token, user_id, application_instance]).start()
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
        pass
    
if __name__ == '__main__':
    print('Trying to open ms teams')
    user_id = 1
    token = 'c4e2d7ae80175496dd9ed92feb2433c52050cf995c7ee17d513fb7c6f60aea3ab18019f7f772c3f47f26482c00e73ba54e4f1f15bc5e705bd1c36e543daea8b7327c215b70ea0e105f060e4e8e2e5e69a61dc89ab7cce1a643c8fbc2be2bbf66d51ede4b4d670b3bce2f4ac4e165c8bcf613ce7bfa2548c8cb5a8b187f4f42ae'
    open_teams(token, user_id, application_instance)

    '''
    print('Trying to start connection ......')
    while True:
        server()
    '''