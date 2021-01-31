import urllib.request
import ssl
import json
myssl = ssl.create_default_context();
myssl.check_hostname=False
myssl.verify_mode=ssl.CERT_NONE
def sendHTTPPost(url: str,payload: dict[str,str]):
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url,data=data)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    response = urllib.request.urlopen(req,context=myssl)
    return response

def login(url: str, username: str, password: str):
    response = sendHTTPPost(url,{"username":username,"password":password})
    return response

def logout(url: str,cookie: dict[str,str]):
    response = sendHTTPPost(url,cookie)
    return response

def getPayload(httpResponse):
    return json.loads(httpResponse.read().decode('utf-8'))

def test_login_logout():
    response=login("https://35.189.171.185:30000/login","test","123")
    cookie=getPayload(response)
    assert 'serialNum' in cookie
    assert 'identifier' in cookie
    assert 'status' in cookie
    assert cookie['status']=='success'
    assert response.status==200
    response=logout("https://35.189.171.185:30000/logout",cookie)
    assert response.status==200
