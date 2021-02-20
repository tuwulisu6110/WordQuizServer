from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
class webTestModule:
    def __init__(self,initPage:str):
        self.initWebdriver(initPage)
    def initWebdriver(self,initPage:str):
        self.service = Service('D:\webdriver\chromedriver.exe')
        self.service.start()
        capabilities = {'acceptSslCerts': True}
        self.driver = webdriver.Remote(self.service.service_url,capabilities)
        self.driver.implicitly_wait(5)
        self.driver.get('https://35.189.171.185:30000/loginLobby')
        #return driver
    def login(self,username:str,password:str):
        usernameTextField=self.driver.find_element_by_id('usernameText')
        usernameTextField.send_keys(username)
        passwordTextField=self.driver.find_element_by_id('passwordText')
        passwordTextField.send_keys(password)
        loginButton=self.driver.find_element_by_xpath("//input[@value='login']")
        loginButton.click()
    def logout(self):
        self.driver.find_element_by_id('logoutNav').click()
    def close(self):
        self.driver.quit()