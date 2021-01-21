# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify
from flask import abort
from flask import url_for, redirect, render_template
import os

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/favicon.ico')
def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')



def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
                   for root_path, dirs, files in os.walk(folder)
                   for f in files))

'''above is server model, following is webpage'''

def getUserManagementURL(request):
    return request.url_root.replace("5000","5001")#.replace("https","http")

def getAddNewWordURL(request):
    return request.url_root.replace("5000","5002")#.replace("https","http")

def getListWordURL(request):
    return request.url_root.replace("5000","5003")#.replace("https","http")

def getQuizURL(request):
    return request.url_root.replace("5000","5004")#.replace("https","http")

@app.route('/loginLobby',methods = {'GET'})
def loginHttpPage():
    userManagementURL=getUserManagementURL(request)
    return render_template('loginLobby.html').replace("%userManagementURL%",userManagementURL)

@app.route('/home',methods = {'GET'})
def home():
    userManagementURL=getUserManagementURL(request)
    return render_template('home.html').replace("%userManagementURL%",userManagementURL)

@app.route('/addNewWordPage', methods = {'GET'})
def addNewWordPage():
    addNewWordURL = getAddNewWordURL(request)
    return render_template('addNewWordPage.html').replace("%addNewWordURL%",addNewWordURL)
    
@app.route('/searchWordPage', methods = {'GET'})
def searchWordPage():
    addNewWordURL = getAddNewWordURL(request)
    listWordURL = getListWordURL(request)
    return render_template('searchWordPage.html').replace("%addNewWordURL%",addNewWordURL).replace("%listWordURL%",listWordURL)
@app.route('/wordQuizPage', methods = {'GET'})
def wordQuizPage():
    quizURL = getQuizURL(request)
    return render_template('wordQuizPage.html').replace("%quizURL%",quizURL)
@app.route('/listWordPage', methods = {'GET'})
def listWordPage():
    addNewWordURL = getAddNewWordURL(request)
    listWordURL = getListWordURL(request)
    return render_template('listWordPage.html').replace("%addNewWordURL%",addNewWordURL).replace("%listWordURL%",listWordURL)

if __name__ == '__main__':
    app.run(host='0.0.0.0',ssl_context=('cert.pem', 'key.pem'))
