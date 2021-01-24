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
    return request.url_root#.replace("30000","30001")#.replace("https","http")

def getAddNewWordURL(request):
    return request.url_root#.replace("5000","5002")#.replace("https","http")

def getListWordURL(request):
    return request.url_root#.replace("5000","5003")#.replace("https","http")

def getQuizURL(request):
    return request.url_root#.replace("5000","5004")#.replace("https","http")

@app.route('/',methods = {'GET'})
def dummy():
    print("Someone access dummy")
    return "This is a dummy."

@app.route('/loginLobby',methods = {'GET'})
def loginHttpPage():
    return render_template('loginLobby.html')

@app.route('/home',methods = {'GET'})
def home():
    return render_template('home.html')

@app.route('/addNewWordPage', methods = {'GET'})
def addNewWordPage():
    return render_template('addNewWordPage.html')
    
@app.route('/searchWordPage', methods = {'GET'})
def searchWordPage():
    return render_template('searchWordPage.html')
@app.route('/wordQuizPage', methods = {'GET'})
def wordQuizPage():
    return render_template('wordQuizPage.html')
@app.route('/listWordPage', methods = {'GET'})
def listWordPage():
    return render_template('listWordPage.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
