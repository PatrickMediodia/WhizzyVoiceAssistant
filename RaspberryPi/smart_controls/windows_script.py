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
        time.sleep(1)
        sess = winrm.Session(DOMAIN, auth=(USERNAME, PASSWORD), transport='ntlm')
        result = sess.run_cmd(f'cd / && cd Users/Pat/Documents/WhizzyVoiceAssistant/Terminal/windows && login_script.bat {username} {password}')
        print(result)
        print('\nCredentials changed\n')
        return True
        
    except Exception as e:
        print('Cannot connect to terminal')
        return False
            
def shutdown_terminal():
    try:
        time.sleep(1)
        sess = winrm.Session(DOMAIN, auth=(USERNAME, PASSWORD), transport='ntlm')
        result = sess.run_cmd(f'cd / && cd Users/Pat/Documents/WhizzyVoiceAssistant/Terminal/windows && shutdown_script.bat')
        print(result)
        print('\nTerminal turned off\n')
        return True
    
    except Exception as e:
        print('Cannot connect to terminal')
        return False
            
def check_terminal_status():
    try:
        time.sleep(1)
        sess = winrm.Session(DOMAIN, auth=(USERNAME, PASSWORD), transport='ntlm')
        result = sess.run_cmd(f'ipconfig')
        return True
    
    except Exception as e:
        return False