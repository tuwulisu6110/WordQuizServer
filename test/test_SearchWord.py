from httpTool import getPayload
from WebApi import loginCookie,searchWord,deleteWord
from config import config
import pytest

@pytest.mark.dependency(
    depends=["test_AddWord.py::test_add_new_word"],
    scope='session'
)
def test_search_delete_word(loginCookie):
    wordPayload={"word":"test"}
    response=searchWord(loginCookie,wordPayload)
    assert response.status==200
    jsonResponse=getPayload(response)
    assert jsonResponse["status"]=="success"
    wordList=[aWord['word'] for aWord in jsonResponse['words']]
    assert "test" in wordList
    for aWord in jsonResponse['words']:
        payload={"wordId":aWord['id']}
        response=deleteWord(loginCookie,payload)
        assert response.status==200


    