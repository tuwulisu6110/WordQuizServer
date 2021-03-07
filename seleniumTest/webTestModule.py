from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from ConfigLoader import ConfigLoader
from HomePage import HomePage
import pytest
class WebTestModule:
    def __init__(self,initPage:str = None):
        configLoader = ConfigLoader()
        self.url=configLoader.getUrl()
        self.driverPath=configLoader.getChromeDriverPath()
        self.initWebdriver(initPage)

    def initWebdriver(self,initPage:str):
        self.service = Service(self.driverPath)
        self.service.start()
        capabilities = {'acceptSslCerts': True}
        self.driver = webdriver.Remote(self.service.service_url,capabilities)
        self.driver.implicitly_wait(5)
        if initPage is None:
            self.driver.get(self.url)
        else:
            self.driver.get(initPage)
        #return driver
    def login(self,username:str,password:str):
        usernameTextField=self.driver.find_element_by_id('usernameText')
        usernameTextField.send_keys(username)
        passwordTextField=self.driver.find_element_by_id('passwordText')
        passwordTextField.send_keys(password)
        loginButton=self.driver.find_element_by_xpath("//input[@value='login']")
        loginButton.click()
        return HomePage(self)

    def logout(self):
        self.driver.find_element_by_id('logoutNav').click()
    def close(self):
        self.driver.quit()
@pytest.fixture
def webTestInst():
    webTestInst=WebTestModule()
    yield webTestInst
    webTestInst.close()
