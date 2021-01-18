# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify
from flask import abort
import urllib2
import sqlite3
from random import randint
import time
from functools import wraps
from flask import url_for, redirect, render_template
import os

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

def getSourceNameTable(sourceTableName):
    sourceNameRows = query_db('select * from '+sourceTableName)
    sourceNameTable = {-1:''}
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
            'correct':row['correct'],
            'sourceId':row['sourceId']}
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
                if request.json[tag] is None:
                    print 'request['+tag+'] is null'
                    return jsonify({'status':'null parameter : ' + tag}),399
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

@app.route('/favicon.ico')
def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')




    


@app.route('/deleteWord',methods = {'POST'})
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

@app.route('/updateWord',methods = {'POST'})
@checkRequestValid(tagList = 
        ['word','reading','meaning','sourceId','page','sentence','wordId'])
@checkTimeStamp
def updateWord():
    wordTableName = request.json['username']+"_words"
    wordInfo = []
    wordInfo.append(request.json['word'])
    wordInfo.append(request.json['reading'])
    wordInfo.append(request.json['meaning'])
    wordInfo.append(request.json['sourceId'])
    wordInfo.append(request.json['page'])
    wordInfo.append(request.json['sentence'])
    wordInfo.append(request.json['wordId'])
    sql = 'update '+wordTableName+''' set 
    word = ?, 
    reading = ?, 
    description = ?, 
    sourceId = ?, 
    page = ?, 
    sentence = ? where id is ?;'''
    commit_db(sql,wordInfo)
    return jsonify({'status':'success'}),201




'''This search interface should accept the search target column, but that's too compelx . So if this function want to refactor pls consider the more general way instead of hard coding'''
@app.route('/searchWordByWordAndReading',methods = {'POST'})
@checkRequestValid(tagList = ['word'])
@checkTimeStamp
def searchWordOld():
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

def checkConditionListValid(conditionList):
    validColume = ['word','reading','sourceId']
    validConditionType = ['contain','match']
    mustContainTag = ['colume','target','conditionType']
    for condition in conditionList:
        for tag in mustContainTag:
            if not tag in condition:
                r = 'condition : '+str(condition)+' lost tag : '+ tag
                print r
                return r
        if not condition['colume'] in validColume:
            r = 'colume in '+str(condition)+' is not valid. validColume : '+str(validColume)
            print r
            return r
        if not condition['conditionType'] in validConditionType:
            r = 'conditionType in '+str(condition)+' is not valid. validConditionType : '+str(validConditionType)
            print r
            return r
    return 'valid'

def assembleConditionsToSQL(tableName,conditionList):
    length = len(conditionList)
    if length == 0:
        return ''
    sql = 'select * from '+ tableName + ' where'
    for condition in conditionList:
        if condition['conditionType'] == 'contain':
            verb = ' like '
            target = '"%'+condition['target']+'%"'
        elif condition['conditionType'] == 'match':
            verb = ' is '
            target = '"'+condition['target']+'"'
        sqlToken = ' ' + condition['colume'] + verb + target
        sql += sqlToken + ' or'
    sql = sql[:-3]
    return sql


@app.route('/searchWord',methods = {'POST'})
@checkRequestValid(tagList = ['conditionList'])
@checkTimeStamp
def searchWord():
    wordTableName = request.json['username']+'_words'
    sourceTableName = request.json['username']+'_sources'
    conditionList = request.json['conditionList']
    r = checkConditionListValid(conditionList)
    if r != 'valid':
        response = {'status':"error","detail":r}
        return jsonify(response),199
    
    sql = assembleConditionsToSQL(wordTableName,conditionList)
    rows = query_db(sql)
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










def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
                   for root_path, dirs, files in os.walk(folder)
                   for f in files))

'''above is server model, following is webpage'''

@app.route('/loginLobby',methods = {'GET'})
def loginHttpPage():
    return render_template('loginLobby.html')

@app.route('/home',methods = {'GET'})
def home():
    return render_template('home.html',lastUpdated=dir_last_updated('static'))

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
