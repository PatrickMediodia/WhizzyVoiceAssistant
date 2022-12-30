'''
pip install pywinauto
'''

import time
import pywinauto

from pywinauto.application import Application
from pywinauto.keyboard import send_keys

application_address = 'C:\\Users\\Pat\\AppData\\Local\\Microsoft\\Teams\\current\\Teams.exe'

app = Application().start(cmd_line=application_address)
time.sleep(1)
