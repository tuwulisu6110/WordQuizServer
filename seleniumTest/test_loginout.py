import time
import pytest
from selenium.common.exceptions import NoSuchElementException
from WebTestModule import webTestInst


def test_login_logout(webTestInst):
    webTestInst.login("test","123")
    
    try:
        webTestInst.driver.find_element_by_id('logoutNav')
    except NoSuchElementException:
        assert False, "logout button not found!"
#    time.sleep(5)
    webTestInst.logout()
    
