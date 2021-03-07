from httpTool import getPayload
from WebApi import login,logout



def test_login_logout():
    response=login("test","123")
    cookie=getPayload(response)
    assert 'serialNum' in cookie
    assert 'identifier' in cookie
    assert 'status' in cookie
    assert cookie['status']=='success'
    assert response.status==200
    response=logout(cookie)
    assert response.status==200
