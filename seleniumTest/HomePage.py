from WebPage import WebPage
from AddNewWordPage import AddNewWordPage
from ListWordPage import ListWordPage
from selenium.common.exceptions import NoSuchElementException
class HomePage(WebPage):
    def navToAddNewWordPage(self):
        try:
            self.webTestModule.driver.find_element_by_id('addNewWordSectionNav').click()
        except NoSuchElementException:
            assert False, "add new word bar item not found!"
        return AddNewWordPage(self.webTestModule)
        
    def navListWordPage(self):
        try:
            self.webTestModule.driver.find_element_by_id('listAllWordSectionNav').click()
        except NoSuchElementException:
            assert False, "list word bar item not found!"
        return ListWordPage(self.webTestModule)