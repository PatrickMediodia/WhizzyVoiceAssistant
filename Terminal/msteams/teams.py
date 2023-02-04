import time
import pywinauto
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from pywinauto import mouse
import os
import wmi
from dotenv import load_dotenv

load_dotenv()

MSTEAMS_USERNAME = os.getenv('MSTEAMS_USERNAME')
MSTEAMS_PASSWORD = os.getenv('MSTEAMS_PASSWORD')

f = wmi.WMI()

def start_teams():
    app = Application(backend='uia').start(
        cmd_line=r'C:\Users\Pat\AppData\Local\Microsoft\Teams\Update.exe --processStart "Teams.exe"')
    time.sleep(5)

    # Get started button
    pywinauto.mouse.click(button='left', coords=(842, 562))
    time.sleep(5)

    # login Credentials -- Email
    pywinauto.keyboard.send_keys(MSTEAMS_USERNAME)
    time.sleep(2)

    # Next Button
    pywinauto.mouse.click(button='left', coords=(1083, 627))
    time.sleep(5)

    # login Credentials -- Password
    pywinauto.keyboard.send_keys(MSTEAMS_PASSWORD)
    time.sleep(2)

    # Sign In Button
    pywinauto.mouse.click(button='left', coords=(1081, 590))
    time.sleep(2)

    # Text Verification Button
    #pywinauto.mouse.click(button='left', coords=(950, 440))
    #time.sleep(2)

start_teams()