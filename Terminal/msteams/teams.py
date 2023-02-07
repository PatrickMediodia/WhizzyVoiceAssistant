import os
import sys
import time
import threading
import pywinauto
import subprocess
from pywinauto import mouse
from dotenv import load_dotenv
from pywinauto.keyboard import send_keys
from pywinauto.application import Application
from credentials import get_teams_account_credentials

def open_teams(token, user_id):
    #run powershell script
    close_teams()
    
    print('\nOpening teams .....\n')

    #get account details from database in another thread
    account_details = {}
    account_thread = threading.Thread(target=get_teams_account_credentials, args=[token, user_id, account_details], daemon=True)
    account_thread.start()

    app = Application(backend='uia').start(fr'C:\Users\{os.getlogin()}\AppData\Local\Microsoft\Teams\Update.exe --processStart "Teams.exe"')
    time.sleep(5)

    # Get started button
    mouse.click(button='left', coords=(842, 562))
    time.sleep(5)

    #wait to get account details
    account_thread.join()
    
    if account_details.get('email') is None or account_details.get('password') is None:
        print('No credentials given')
        return
        
    # login Credentials -- Email
    send_keys(account_details['email'])
    time.sleep(2)

    # Next Button
    mouse.click(button='left', coords=(1083, 627))
    time.sleep(5)

    # login Credentials -- Password
    send_keys(account_details['password'])
    time.sleep(2)

    # Sign In Button
    mouse.click(button='left', coords=(1080, 592))
    mouse.click(button='left', coords=(1100, 560))
    time.sleep(5)

    # Text Verification Button
    mouse.click(button='left', coords=(950, 440))
    time.sleep(2)
    
def close_teams():
    print('\nClosing teams instances .....\n')

    #run powershell script
    p = subprocess.Popen(
        r'powershell.exe -ep bypass -File C:\Users\Public\Documents\WhizzyVoiceAssistant\Terminal\msteams\teams_logout.ps1',
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.STDOUT
    )
    p.communicate()