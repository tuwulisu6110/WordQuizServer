import time
import pytest
from selenium.common.exceptions import NoSuchElementException
from webTestModule import webTestInst


@pytest.mark.dependency(
    depends=["test_addNewWord.py::test_addNewWord"],
    scope='session'
)
def test_deleteWord(webTestInst):
    webTestInst.login("test","123")
    
    try:
        webTestInst.driver.find_element_by_id('listAllWordSectionNav').click()
    except NoSuchElementException:
        assert False, "list word bar item not found!"
    try:
        webTestInst.driver.find_element_by_id('searchWordText').send_keys("test")
    except NoSuchElementException:
        assert False, "search word text field not found!"
   
    try:
        webTestInst.driver.find_element_by_xpath("//input[@value='Search Word']").click()
    except NoSuchElementException:
        assert False, "search word button not found!"
    time.sleep(5)# wait for the table is refreshed
    try:
        webTestInst.driver.find_element_by_xpath("//td[contains(text(),'test')]")
    except NoSuchElementException:
        assert False, "test word not found!"
    
    try:
        
        webTestInst.driver.find_element_by_xpath("//input[@value='delete']").click()
    except NoSuchElementException:
        assert False, "delete button not found!"

    webTestInst.driver.find_element_by_id('listAllWordSectionNav').click()

    webTestInst.logout()
    
