from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify
from flask import abort
from flask import url_for, redirect, render_template
import sqlite3
from random import randint
from functools import wraps
from DBAccessor import query_db, commit_db_and_get_lastId, commit_db
from SharedFunction import checkRequestValid
from flask_cors import CORS,cross_origin
import time

app = Flask(__name__)
app.config['DEBUG'] = True


'''this is for clearing cookies at program begin, if this program need to run in long time, this program should add a cookie collection function'''
def createRamdomString(length=10):
    rString = ""
    for num in range(1,length):
        rString += chr(97+randint(0,25))
    return rString



@app.route('/login',methods = ['POST','OPTIONS'])
@cross_origin()
@checkRequestValid(tagList = ['username','password'])
def login():
    user = query_db('SELECT * FROM account WHERE USERNAME = ?',
                [request.json['username']], one=True)
    if user is None:
        r = {'status':'username error'}
    elif user['password'] != request.json['password']:
        r = {'status':'password error'}
    else:
        r = {'status':'success'}
        rString = createRamdomString(10)
        expiredTime = int(time.time())+3600
        lastId = commit_db_and_get_lastId('''insert into cookies 
                (rString, expiredTime, username)values (?,?,?)''',
                [rString,expiredTime,request.json['username']])
        r['serialNum'] = lastId
        r['identifier'] = rString
    return jsonify( r ),200

@app.route('/logout',methods = ['POST','OPTIONS'])
@cross_origin()
@checkRequestValid(tagList=['serialNum','identifier'])
def logout():
    serialNum = request.json['serialNum']
    identifier = request.json['identifier']
    commit_db('delete from cookies where id = ? and rString = ?',
            [serialNum,identifier])
    r={'status':"success"}
    return jsonify(r),200
    
@app.route('/register',methods = ['POST','OPTIONS'])
@cross_origin()
@checkRequestValid(tagList = ['username','password'])
def register():
    if not stringValid(request.json['username']):
        return jsonify({'status':'username invalid'}),202
    if not stringValid(request.json['password']):
        return jsonify({'status':'password invalid'}),202
    user = query_db('select * FROM account where USERNAME = ?',
                [request.json['username']], one=True)
    if user is not None:
        r = {'status':'username existed'}
    else:
        r = {'status':'success'}
        commit_db('insert into account values(?,?)',
                [request.json['username'],request.json['password']])
        try:
            sourcesTableName = request.json['username']+'_sources'
            wordsTableName = request.json['username']+'_words'
            
            query1='''create table '''
            query2='''(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            source TEXT NOT NULL
                    );'''
            commit_db(query1 + sourcesTableName + query2)
            commit_db('''create table '''+wordsTableName+'''(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            word TEXT NOT NULL,
            reading TEXT,
            description TEXT,
            sourceId INTEGER,
            sentence TEXT,
                    page TEXT,
                    pick INTEGER DEFAULT 0,
                    correct INTEGER DEFAULT 0
            );''')
        except sqlite3.Error as e:
            print('er: %s' % e.args[0])
    return jsonify(r),201
def stringValid(s):
    for c in s:
        if not((ord(c) > 64 and ord(c) < 91) or (ord(c) > 96 and ord(c) < 123)or
                (ord(c) > 47 and ord(c) < 58)):
           	return False
    else:
        return True

def clearOldCookies():
    commit_db('delete from cookies where expiredTime < ?',[int(time.time())])
clearOldCookies()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
