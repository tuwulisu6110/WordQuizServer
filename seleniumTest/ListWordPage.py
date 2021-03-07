from WebPage import WebPage
from selenium.common.exceptions import NoSuchElementException
class ListWordPage(WebPage):
    def fillSearchWordText(self,word: str):
        try:
            self.webTestModule.driver.find_element_by_id('searchWordText').send_keys(word)
        except NoSuchElementException:
            assert False, "search word text field not found!"
    def clickSearchButton(self):
        try:
            self.webTestModule.driver.find_element_by_xpath("//input[@value='Search Word']").click()
        except NoSuchElementException:
            assert False, "search word button not found!"
    def locateWord(self,word:str):
        try:
            self.webTestModule.driver.find_element_by_xpath("//td[contains(text(),'"+word+"')]")
        except NoSuchElementException:
            assert False, word+" word not found!"
    def checkWordNotExist(self,word:str):
        try:
            self.webTestModule.driver.find_element_by_xpath("//td[contains(text(),'"+word+"')]")
        except NoSuchElementException:
            return
        assert False, word+" word found!"
    def deleteWord(self):
        try:
            self.webTestModule.driver.find_element_by_xpath("//input[@value='delete']").click()
        except NoSuchElementException:
            assert False, "delete button not found!"
    
    