import json
from httpTool import sendHTTPPost,getPayload
from config import config



def login(url: str, username: str, password: str):
    response = sendHTTPPost(url,{"username":username,"password":password})
    return response

def logout(url: str,cookie: dict[str,str]):
    response = sendHTTPPost(url,cookie)
    return response



def test_login_logout():
    response=login(config["DEFAULT"]["url"]+"/login","test","123")
    cookie=getPayload(response)
    assert 'serialNum' in cookie
    assert 'identifier' in cookie
    assert 'status' in cookie
    assert cookie['status']=='success'
    assert response.status==200
    response=logout(config["DEFAULT"]["url"]+"/logout",cookie)
    assert response.status==200
