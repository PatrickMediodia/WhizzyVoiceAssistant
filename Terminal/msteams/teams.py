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
    flag = 0
    # Iterating through all the running processes
    for process in f.Win32_Process():
        if "Teams.exe" == process.Name:
            print("Application is already Running")
            flag = 1
            break
    if flag == 0:
        # open MS Teams
        app = Application(backend='uia').start(
            cmd_line=r'C:\Users\Pat\AppData\Local\Microsoft\Teams\Update.exe --processStart "Teams.exe"')
        time.sleep(3)

        # Use another account or sign up Button
        pywinauto.mouse.click(button='left', coords=(977, 822))
        time.sleep(5)

        # login Credentials -- Email
        pywinauto.keyboard.send_keys("")
        time.sleep(2)

        # Next Button
        pywinauto.mouse.click(button='left', coords=(1084, 648))
        time.sleep(5)

        # login Credentials -- Password
        pywinauto.keyboard.send_keys("Dominican1234@")
        time.sleep(2)

        #Sign In Button
        pywinauto.mouse.click(button='left', coords=(1084, 613))
        time.sleep(2)

        # Text Verification Button
        pywinauto.mouse.click(button='left', coords=(939, 464))
        time.sleep(2)

def exit_teams():
    flag = 0
    # Iterating through all the running processes
    for process in f.Win32_Process():
        if "Teams.exe" == process.Name:
            os.system('taskkill /f /im "Teams.exe"')
            flag = 1
            break
    if flag == 0:
        print("Application is not Running")

exit_teams()
start_teams()