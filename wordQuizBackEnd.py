# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify
from flask import abort
import sqlite3
from cors import crossdomain
from random import randint
import time
from functools import wraps
from flask import url_for, redirect, render_template

app = Flask(__name__)
app.config['DEBUG'] = True

DATABASE = 'wordQuizData.db'
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def query_db(query, args=(), one=False):
    db = sqlite3.connect(DATABASE)
    db.row_factory = make_dicts
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    db.close()
    return (rv[0] if rv else None) if one else rv

def commit_db_and_get_lastId(query, args=()):
    db = sqlite3.connect(DATABASE)
    cur = db.execute(query, args)
    id = cur.lastrowid
    db.commit()
    db.close()
    return id

def commit_db(query, args=()):
    db = sqlite3.connect(DATABASE)
    db.execute(query, args)
    db.commit()
    db.close()
def clearOldCookies():
    commit_db('delete from cookies where expiredTime < ?',[int(time.time())])
clearOldCookies()
'''this is for clearing cookies at program begin, if this program need to run in long time, this program should add a cookie collection function'''
def createRamdomString(length=10):
    rString = ""
    for num in range(1,length):
        rString += chr(97+randint(0,25))
    return rString
def getSourceNameTable(sourceTableName):
    sourceNameRows = query_db('select * from '+sourceTableName)
    sourceNameTable = {'-1':''}
    '''this is for the condition that no sourceName in some words'''
    if sourceNameRows is not None:
        for snRow in sourceNameRows:
            sourceNameTable[snRow['id']] = snRow['source']
    return sourceNameTable

def generateRandomIdSet(num,maxLimit):
    rIds = []
    while len(rIds)<num:
        r = randint(0,maxLimit)
        while r in rIds:
            r = randint(0,maxLimit)
        rIds.append(r)
    return rIds
def generateJsonWord(row,sourceNameTable):
    if row['pick']==0:
        rate = 0
    else:
        rate = float(row['correct']) / row['pick']
    aWord = {'word':row['word'],
            'reading':row['reading'],
            'meaning':row['description'],
            'sourceName':sourceNameTable[row['sourceId']],
            'sentence':row['sentence'],
            'page':row['page'],
            'id':row['id'],
            'rate':rate,
            'pick':row['pick'],
            'correct':row['correct']}
    return aWord

def checkRequestValid(tagList=[]):
    def decorator_checkRequestValid(func):
        @wraps(func)
        def func_checkRequestValid():
	    if not request.json:
	        abort(400)
	    for tag in tagList:
	        if not tag in request.json:
                    print 'no tag : ' + tag
	            return jsonify({'status':'lost params : '+tag}),399
            return func()
        return func_checkRequestValid
    return decorator_checkRequestValid

def checkTimeStamp(func):
    @wraps(func)
    @checkRequestValid(tagList=['serialNum','identifier'])
    def func_checkTimeStamp():
        serialNum = request.json['serialNum']
        identifier = request.json['identifier']
        stamp =  query_db('select * from cookies where id = ? and rString = ?',
                [serialNum,identifier],one= True)
        if stamp is None:
            return jsonify({"status":"without cookie"}),299
        elif int(stamp['expiredTime']) < int(time.time()):
            commit_db('delete from cookies where id = ? and rString = ?',
                    [serialNum,identifier])
            return jsonify({"status":"time expired"}),398
        else:
            return func()
    return func_checkTimeStamp

@app.route('/login',methods = ['POST','OPTIONS'])
@crossdomain(origin='*',headers='Content-type')
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
    return jsonify( r ),201

def stringValid(s):
    for c in s:
        if not((ord(c) > 64 and ord(c) < 91) or (ord(c) > 96 and ord(c) < 123)or
                (ord(c) > 47 and ord(c) < 58)):
           	return False
    else:
        return True

@app.route('/register',methods = ['POST','OPTIONS'])
@crossdomain(origin='*',headers='Content-type')
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
        except sqlite3.Error ,e:
            print 'er: %s' % e.args[0]
    return jsonify(r),201

@app.route('/addSource',methods = {'POST'})
@crossdomain(origin='*',headers='Content-type')
@checkRequestValid(tagList = ['username','source'])
@checkTimeStamp
def addSource():
        username = request.json['username']
        sourceName = request.json['source']
	id = commit_db_and_get_lastId('insert into '+
                username+'_sources' +' (source) values (?)',[sourceName])
        return jsonify({'status':'success','lastId':id}),201

@app.route('/listSource',methods = {'POST'})
@crossdomain(origin='*',headers='Content-type')
@checkRequestValid(tagList = ['username'])
@checkTimeStamp
def listSource():	
    rows = query_db('select * from '+request.json['username']+'_sources')
    sources = {}
    if rows is not None:
        for row in rows:
            sources[row['id']] = row['source']
    r = {'sources':sources}
    r['status']='success'
    return jsonify(r),201

@app.route('/deleteWord',methods = {'POST'})
@crossdomain(origin='*',headers='Content-type')
@checkRequestValid(tagList = ['wordId'])
@checkTimeStamp
def deleteWord():
    wordTableName = request.json['username']+'_words'
    row = query_db('select * from ' + wordTableName +' where id = ?'
            ,[request.json['wordId']],one=True)
    if row is not None:
        commit_db('delete from '+wordTableName+' where id = ?',
                [request.json['wordId']])
        return jsonify({'status':'success'}),201
    else:
        return jsonify({'status':'cant find word:'+
            str(request.json['wordId'])}),199

@app.route('/addWord',methods = {'POST'})
@crossdomain(origin='*',headers='Content-type')
@checkRequestValid(tagList = 
        ['word','reading','meaning','sourceId','page','sentence'])
@checkTimeStamp
def addWord():
    wordTableAddr = request.json['username']+"_words"
    wordInfo = []
    wordInfo.append(request.json['word'])
    wordInfo.append(request.json['reading'])
    wordInfo.append(request.json['meaning'])
    wordInfo.append(request.json['sourceId'])
    wordInfo.append(request.json['page'])
    wordInfo.append(request.json['sentence'])
    commit_db('insert into '+ wordTableAddr +
            ''' (word,reading,description,sourceId,page,sentence) 
            values (?,?,?,?,?,?)''',wordInfo)
    return jsonify({'status':'success'}),201


'''This search interface should accept the search target column, but that's too compelx . So if this function want to refactor pls consider the more general way instead of hard coding'''
@app.route('/searchWordByWordAndReading',methods = {'POST'})
@crossdomain(origin='*',headers='Content-type')
@checkRequestValid(tagList = ['word'])
@checkTimeStamp
def searchWord():
    wordTableName = request.json['username']+'_words'
    sourceTableName = request.json['username']+'_sources'
    if not request.json['word']:
        rows = query_db('select * from '+ wordTableName)
    else:
        queryWord = request.json['word']
        realCondition = '%'+queryWord+'%'
        rows = query_db('select * from '+ wordTableName +
             ' where word like ? or reading like ?',
             [realCondition,realCondition])
        '''hard coding here'''
    sourceNameTable = getSourceNameTable(sourceTableName)
    wordList = []
    if rows is not None:
        for row in rows:
            aWord = generateJsonWord(row,sourceNameTable)
            wordList.append(aWord)
    return jsonify({'status':'success','words':wordList}),201


@app.route('/randomWord',methods = ['POST'])
@checkRequestValid(tagList = ['num'])
@checkTimeStamp
def randomWord():
    wordTableName = request.json['username'] + '_words'
    sourceTableName = request.json['username']+'_sources'
    num = request.json['num']
    rows = query_db('select * from '+ wordTableName)
    if num > len(rows):
        return jsonify({'status':'num is over the data size'}),198
    rSet = generateRandomIdSet(num,len(rows)-1)
    sourceNameTable = getSourceNameTable(sourceTableName)
    wordList = []
    for rNum in rSet:
        row = rows[rNum]
        aWord = generateJsonWord(row,sourceNameTable)
        wordList.append(aWord)
    return jsonify({'status':'success','words':wordList}),201

@app.route('/recordAnswerResult',methods = ['POST'])
@checkRequestValid(tagList = ['wordId','result'])
@checkTimeStamp
def recordAnswerResult():
    wordTableName = request.json['username'] + '_words'
    if request.json['result'] == 1:
        correctStr = ', correct = correct + 1'
    else:
        correctStr = ''
    commit_db('update '+wordTableName+
            ' set pick = pick+1 '+ correctStr +
            ' where id = ?',[request.json['wordId']])
    return jsonify({'status':'success'}),201

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

if __name__ == '__main__':
    app.run(host='0.0.0.0')
