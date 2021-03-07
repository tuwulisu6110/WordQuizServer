import time
import pytest
from WebTestModule import webTestInst

@pytest.mark.dependency(
    depends=["test_addNewWord.py::test_addNewWord"],
    scope='session'
)
def test_deleteWord(webTestInst):
    homePage=webTestInst.login("test","123")
    
    listWordPage=homePage.navListWordPage()
    listWordPage.fillSearchWordText("test")
    listWordPage.clickSearchButton()
    time.sleep(3)# wait for the table is refreshed
    listWordPage.locateWord("test")
    listWordPage.deleteWord()

    listWordPage.clickSearchButton()
    time.sleep(3)
    listWordPage.checkWordNotExist("test")

    webTestInst.logout()
    
