'''
pip install selenium
pip install webdriver-manager
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()

#window will not close of script will stop
options.add_experimental_option('detach', True)

#remove message of "chrome being controlled by automated test software"
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])

#initialize driver object
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

def blackboard(username, password):
    #open Brwoser
    driver.get('https://mcl.blackboard.com/')
    driver.maximize_window()

    #click on OK in dialog box
    button = driver.find_element(By.ID, 'agree_button').click()

    #fill-up the form
    username_input = driver.find_element(By.ID, 'user_id')
    username_input.send_keys(username)

    password_input = driver.find_element(By.ID, 'password')
    password_input.send_keys(password)

    #click login button
    login_button = driver.find_element(By.ID, 'entry-login')
    login_button.click()
    
#call blackboard function
blackboard('sample username', 'sample password')