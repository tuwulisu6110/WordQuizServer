from WebApi import loginCookie,addNewWord
from config import config
import pytest

@pytest.mark.dependency()
def test_add_new_word(loginCookie):
    wordPayload={"word":"test",
				"reading":"testreading",
                "meaning":"testmeaning",
				"sourceId":"-1",
                "page":"111",
                "sentence":"testsentence"}
    response=addNewWord(loginCookie,wordPayload)
    assert response.status==200
    
    
    
    
    
    
    
    
    