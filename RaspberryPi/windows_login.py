'''
https://stackoverflow.com/questions/38105486/winrm-the-specified-credentials-were-rejected-by-the-server
'''
import winrm

def login_terminal(username, password, domain):
    try:
        sess = winrm.Session('DESKTOP-0K06L79', auth=('username', 'password'))
        result = sess.run_cmd(f'cd / && cd Users/Pat/Documents/WhizzyVoiceAssistant/Terminal && login_script.bat {username} {password} {domain}')
        print(result)
        print('Credentials changed')
    except Exception as e:
        print(e)
        print('An error occured')

#Personal
login_terminal('username', 'password', 'DESKTOP-0K06L79')

#Whizzy
#login_terminal('Whizzy', 'Admin1234@', 'DESKTOP-0K06L79')
