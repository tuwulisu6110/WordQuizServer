import time
import pytest
from WebTestModule import webTestInst
@pytest.mark.dependency()
def test_addNewWord(webTestInst):
    homePage=webTestInst.login("test","123")
    addNewWordPage = homePage.navToAddNewWordPage()
    addNewWordPage.fillWordText("test")
    addNewWordPage.fillReadingText("test_reading")
    addNewWordPage.fillMeaningText("test_meaning")
    addNewWordPage.submitWord()
    webTestInst.logout()
    
