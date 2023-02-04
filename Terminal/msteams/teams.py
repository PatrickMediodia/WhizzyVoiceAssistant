import os
import wmi
import time
import threading
import pywinauto
from pywinauto import mouse
from dotenv import load_dotenv
from pywinauto.keyboard import send_keys
from pywinauto.application import Application
from credentials import get_teams_account_credentials
def open_teams(token, user_id, application_instance):
    #get account details from database in another thread
    account_details = {}
    account_thread = threading.Thread(target=get_teams_account_credentials, args=[token, user_id, account_details], daemon=True)
    account_thread.start()

    app = Application(backend='uia').start(r'C:\Users\Pat\AppData\Local\Microsoft\Teams\Update.exe --processStart "Teams.exe"')
    time.sleep(5)

    # Get started button
    pywinauto.mouse.click(button='left', coords=(842, 562))
    time.sleep(5)

    #wait to get account details
    account_thread.join() 

    # login Credentials -- Email
    pywinauto.keyboard.send_keys(account_details['email'])
    time.sleep(2)

    # Next Button
    pywinauto.mouse.click(button='left', coords=(1083, 627))
    time.sleep(5)

    # login Credentials -- Password
    pywinauto.keyboard.send_keys(account_details['password'])
    time.sleep(2)

    # Sign In Button
    pywinauto.mouse.click(button='left', coords=(1080, 592))
    time.sleep(5)

    # Text Verification Button
    pywinauto.mouse.click(button='left', coords=(950, 440))
    time.sleep(2)