from WebPage import WebPage
from selenium.common.exceptions import NoSuchElementException
class AddNewWordPage(WebPage):
    def fillWordText(self,text:str):
        try:
            self.webTestModule.driver.find_element_by_id('wordText').send_keys(text)
        except NoSuchElementException:
            assert False, "word text field not found!"
    def fillReadingText(self,text:str):
        try:
            self.webTestModule.driver.find_element_by_id('readingText').send_keys(text)
        except NoSuchElementException:
            assert False, "reading text field not found!"
    def fillMeaningText(self,text:str):
        try:
            self.webTestModule.driver.find_element_by_id('meaningText').send_keys(text)
        except NoSuchElementException:
            assert False, "meaning text field not found!"
    def submitWord(self):
        try:
            self.webTestModule.driver.find_element_by_xpath("//input[@value='submit']").click()
        except NoSuchElementException:
            assert False, "submit button not found!"
    