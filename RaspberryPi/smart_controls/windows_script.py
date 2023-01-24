import winrm
import time

'''
set wi-fi connection to private
'''

DOMAIN = '192.168.0.101'
USERNAME = 'Pat'
PASSWORD = 'Admin1234@'

def login_terminal(username, password, domain):
    print('\nTrying to connect to terminal ......\n')
    times_tried = 0
    
    while True:
        try:
            #run in 5 second intervals until successful
            time.sleep(5)
            #use credentials of admin account
            sess = winrm.Session(DOMAIN, auth=(USERNAME, PASSWORD), transport='ntlm')

            #trigger batch script that changes registry on terminal
            result = sess.run_cmd(f'cd / && cd Users/Pat/Documents/WhizzyVoiceAssistant/Terminal/windows && login_script.bat {username} {password} {domain}')
            print('\nCredentials changed\n')
            break
        
        except Exception as e:
            times_tried +=1
            if times_tried == 3:
                print('Cannot connect to terminal')
                times_tried = 0
                
def shutdown_terminal():
    print('\nTrying to shutdown terminal ......\n')
    times_tried = 0
    
    while True:
        try:
            #run in 5 second intervals until successful
            time.sleep(5)
            
            #use credentials of admin account
            sess = winrm.Session(DOMAIN, auth=(USERNAME, PASSWORD), transport='ntlm')
            
            #trigger batch script that changes registry on terminal
            result = sess.run_cmd(f'cd / && cd Users/Pat/Documents/WhizzyVoiceAssistant/Terminal/windows && shutdown_script.bat')
            print('\nTerminal turned off\n')
            break
        
        except Exception as e:
            times_tried +=1
            if times_tried == 3:
                print('Cannot connect to terminal')
                times_tried = 0
                
def check_terminal_status():
    try:
        #establish session
        sess = winrm.Session(DOMAIN, auth=(USERNAME, PASSWORD), transport='ntlm')
        result = sess.run_cmd(f'ipconfig')
        return True
    
    except Exception as e:
        return
    
#shutdown_terminal()

#Admin
#login_terminal('Pat', 'Admin1234@', 'DESKTOP-0K06L79')
            
#Whizzy
#login_terminal('Whizzy', 'Admin1234@', 'DESKTOP-0K06L79')