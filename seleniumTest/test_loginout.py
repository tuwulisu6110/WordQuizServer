import time
from webTestModule import webTestModule
import pytest
from selenium.common.exceptions import NoSuchElementException

@pytest.fixture
def webTestInst():
    webTestInst=webTestModule('https://35.189.171.185:30000/loginLobby')
    yield webTestInst
    webTestInst.close()


def test_login_logout(webTestInst):
    webTestInst.login("test","123")
    
    try:
        webTestInst.driver.find_element_by_id('logoutNav')
    except NoSuchElementException:
        assert False, "logout button not found!"
    webTestInst.logout()
    
