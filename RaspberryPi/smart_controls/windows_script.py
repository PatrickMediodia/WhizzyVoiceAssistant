'''
set wi-fi connection to private
'''

import os
import time
import winrm

DOMAIN = os.environ.get('WINDOWS_DOMAIN')
USERNAME = os.environ.get('WINDOWS_USERNAME')
PASSWORD = os.environ.get('WINDOWS_PASSWORD')

def login_terminal(username, password):
    try:
        time.sleep(3)
        sess = winrm.Session(DOMAIN, auth=(USERNAME, PASSWORD), transport='ntlm')
        result = sess.run_cmd(f'cd / && cd Users/Public/Documents/WhizzyVoiceAssistant/Terminal/windows && login_script.bat {username} {password}')
        
        if 'The operation completed successfully' in result.std_out.decode('utf-8'):
            print('\nCredentials changed\n')
            return True
        else:
            return False
        
    except Exception as e:
        print('Cannot connect to terminal')
        return False
            
def shutdown_terminal():
    try:
        time.sleep(3)
        sess = winrm.Session(DOMAIN, auth=(USERNAME, PASSWORD), transport='ntlm')
        result = sess.run_cmd(f'cd / && cd Users/Public/Documents/WhizzyVoiceAssistant/Terminal/windows && shutdown_script.bat')
        
        if 'Computer turned off' in result.std_out.decode('utf-8'):
            print('\nTerminal turned off\n')
            return True
        else:
            return False
        
    except Exception as e:
        print('Cannot connect to terminal')
        return False