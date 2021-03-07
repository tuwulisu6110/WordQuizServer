from httpTool import sendHTTPPost
from config import config
from httpTool import getPayload
import pytest
@pytest.fixture
def loginCookie():
    cookie=getPayload(login("test","123"))
    cookie["username"]="test"
    cookie["password"]="123"
    yield cookie
    logout(cookie)

def login(username: str, password: str, url: str=config["DEFAULT"]["url"]+"/login"):
    response = sendHTTPPost(url,{"username":username,"password":password})
    return response

def logout(cookie: dict[str,str],url: str=config["DEFAULT"]["url"]+"/logout"):
    response = sendHTTPPost(url,cookie)
    return response
    
def addNewWord(cookie: dict[str,str],payload: dict[str,str],url: str=config["DEFAULT"]["url"]+"/addWord"):
    payload.update(cookie)
    response = sendHTTPPost(url,payload)
    return response
    
def searchWord(cookie: dict[str,str],payload: dict[str,str],url: str=config["DEFAULT"]["url"]+"/searchWordByWordAndReading"):
    payload.update(cookie)
    response = sendHTTPPost(url,payload)
    return response

def deleteWord(cookie: dict[str,str],payload: dict[str,str],url: str=config["DEFAULT"]["url"]+"/deleteWord"):
    payload.update(cookie)
    response = sendHTTPPost(url,payload)
    return response