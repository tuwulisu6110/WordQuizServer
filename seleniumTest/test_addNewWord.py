import time
import pytest
from selenium.common.exceptions import NoSuchElementException
from webTestModule import webTestInst

@pytest.mark.dependency()
def test_addNewWord(webTestInst):
    webTestInst.login("test","123")
    
    try:
        webTestInst.driver.find_element_by_id('addNewWordSectionNav').click()
    except NoSuchElementException:
        assert False, "add new word bar item not found!"
    try:
        webTestInst.driver.find_element_by_id('wordText').send_keys("test")
    except NoSuchElementException:
        assert False, "word text field not found!"
   
    try:
        webTestInst.driver.find_element_by_id('readingText').send_keys("test_reading")
    except NoSuchElementException:
        assert False, "reading text field not found!"

    try:
        webTestInst.driver.find_element_by_id('meaningText').send_keys("test_meaning")
    except NoSuchElementException:
        assert False, "meaning text field not found!"
    
    try:
        webTestInst.driver.find_element_by_xpath("//input[@value='submit']").click()
    except NoSuchElementException:
        assert False, "submit button not found!"


    webTestInst.logout()
    
