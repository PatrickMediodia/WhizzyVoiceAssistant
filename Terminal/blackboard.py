import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from credentials import get_bbl_account_credentials
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

#window will not close of script will stop
options = Options()
options.add_experimental_option('detach', True) 

#remove message of "chrome being controlled by automated test software"
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])

#remove cmd messages/logs
options.add_argument("--log-level=3");

def open_blackboard(token, user_id, application_instance):
    print('\nOpening blackboard .....\n')

    #get account details from database in another thread
    account_details = {}
    account_thread = threading.Thread(target=get_bbl_account_credentials, args=[token, user_id, account_details], daemon=True)
    account_thread.start()

    #initialize driver object
    driver = webdriver.Chrome(service=Service('./drivers/chromedriver.exe'), options=options)
    
    #open Brwoser
    driver.get('https://mcl.blackboard.com/')
    driver.maximize_window()
    driver.find_element(By.ID, 'agree_button').click() #click on OK in dialog box

    #wait to get account details
    account_thread.join() 
    
    #check if there are credentials
    if account_details.get('email') is None or account_details.get('password') is None:
        #return instance to main
        application_instance['blackboard'] = driver
        print('\nNo credentials given\n')
        return

    #fill-up the form
    username_input = driver.find_element(By.ID, 'user_id')
    username_input.send_keys(account_details['email'])
    
    password_input = driver.find_element(By.ID, 'password')
    password_input.send_keys(account_details['password'])

    #click login button
    login_button = driver.find_element(By.ID, 'entry-login')
    login_button.click()
    
    #return instance to main
    application_instance['blackboard'] = driver