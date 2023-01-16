import winrm
import time

def login_terminal(username, password, domain):
    while True:
        try:
            #run in 3 second intervals until successful
            time.sleep(3)
            
            #use credentials of admin account
            sess = winrm.Session('DESKTOP-0K06L79', auth=('Pat', 'Admin1234@'), transport='ntlm')
            print('Session established')
            
            #trigger batch script that changes registry on terminal
            result = sess.run_cmd(f'cd / && cd Users/Pat/Documents/WhizzyVoiceAssistant/Terminal/windows && login_script.bat {username} {password} {domain}')
            print('Credentials changed')
            break
        
        except Exception as e:
            print('An error has occured')

#Admin
#login_terminal('Pat', 'Admin1234@', 'DESKTOP-0K06L79')
            
#Whizzy
#login_terminal('Whizzy', 'Admin1234@', 'DESKTOP-0K06L79')