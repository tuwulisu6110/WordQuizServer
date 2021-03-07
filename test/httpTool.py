import ssl
import json
import urllib.request
myssl = ssl.create_default_context();
myssl.check_hostname=False
myssl.verify_mode=ssl.CERT_NONE
def sendHTTPPost(url: str,payload: dict[str,str]):
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url,data=data)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    response = urllib.request.urlopen(req,context=myssl)
    return response
def getPayload(httpResponse)->dict[str,str]:
    return json.loads(httpResponse.read().decode('utf-8'))