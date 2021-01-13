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
'''this is for clearing cookies at program begin, if this program need to run in long time, this program should add a cookie collection function'''
def createRamdomString(length=10):
    rString = ""
    for num in range(1,length):
        rString += chr(97+randint(0,25))
    return rString
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



@app.route('/login',methods = ['POST','OPTIONS'])
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

@app.route('/logout',methods = ['POST','OPTIONS'])
@checkRequestValid(tagList=['serialNum','identifier'])
def logout():
    serialNum = request.json['serialNum']
    identifier = request.json['identifier']
    commit_db('delete from cookies where id = ? and rString = ?',
            [serialNum,identifier])
    r={'status':"success"}
    return jsonify(r),201

def stringValid(s):
    for c in s:
        if not((ord(c) > 64 and ord(c) < 91) or (ord(c) > 96 and ord(c) < 123)or
                (ord(c) > 47 and ord(c) < 58)):
           	return False
    else:
        return True

@app.route('/favicon.ico')
def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/register',methods = ['POST','OPTIONS'])
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
@checkRequestValid(tagList = ['username','source'])
@checkTimeStamp
def addSource():
        username = request.json['username']
        sourceName = request.json['source']
	id = commit_db_and_get_lastId('insert into '+
                username+'_sources' +' (source) values (?)',[sourceName])
        return jsonify({'status':'success','lastId':id}),201

@app.route('/listSource',methods = {'POST'})
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

@app.route('/deleteSource',methods = ['POST'])
@checkRequestValid(tagList = ['username','sourceId','deleteSourceMode'])
@checkTimeStamp
def deleteSource():
    sourceTableName = request.json['username'] + '_sources'
    wordTableName = request.json['username'] + '_words'
    sourceId = request.json['sourceId']
    deleteSourceMode = request.json['deleteSourceMode']
    
    if deleteSourceMode != '0' and deleteSourceMode != '1':
        print 'error deleteSourceMode = '+deleteSourceMode
        return jsonify({'status':'error deleteSourceMode = '
            + deleteSourceMode}),199
    
    row = query_db('select * from '+ sourceTableName +' where id = ?'
            ,[sourceId],one=True)
    if row is not None:
        commit_db('delete from '+ sourceTableName + ' where id = ?',
                [sourceId])
    else:
        return jsonify({'status':'cant find source id:'+
            str(sourceId)}),199
    rowCount =  query_db('select count(*) from '+ wordTableName + ' where sourceId = ?'
                                ,[sourceId],one=True)
    affectedWordNum = str(rowCount['count(*)'])
    r={'status':'success'}
    if deleteSourceMode == '0':
        commit_db('delete from '+ wordTableName + ' where sourceId = ?',
                [sourceId])
        r['detail']=affectedWordNum+' words deleted.'
        return jsonify(r),200
    elif deleteSourceMode == '1':
        commit_db('update '+wordTableName + 
                ' set sourceId = -1 where sourceId = ?',[sourceId])
        r['detail']=affectedWordNum+' words updated.'
        return jsonify(r),200
    


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

@app.route('/addWord',methods = {'POST'})
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




def eliminateNonWordChar(str):
    nonWordList=['・']
    for nonWord in nonWordList:
        str = str.replace(nonWord,'')
    return str
MozillaFakeHeader = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                     'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                     'Accept-Encoding': 'none',
                     'Accept-Language': 'en-US,en;q=0.8',
                     'Connection': 'keep-alive'}
gooURLFront = "http://dictionary.goo.ne.jp/srch/"
gooURLMiddleAll = "all/"
gooURLMiddleJn2 = "jn/"
gooURLTail = "/m0u/"
right ='】'
left ='【'
singleResultPage = 1
multipleResultPage = 2
notFoundPage=3

@app.route('/listAllReadingByWord',methods = ['POST'])
@checkRequestValid(tagList = ['word'])
@checkTimeStamp
def listReadingByWord():
    readingList = []
    word = request.json['word'].encode('utf-8')
    wordEnd = left+word+right
    wordBegin = '"title search-ttl-a"'
    cursor = 0
    req = urllib2.Request(gooURLFront+gooURLMiddleAll+word+gooURLTail, headers=MozillaFakeHeader)
    page = urllib2.urlopen(req).read()
    while(cursor!=-1):
        posEnd = page.find(wordEnd,cursor)
        if posEnd==-1:
            break
        posBegin = page.find(wordBegin,posEnd-50)
        posBegin = posBegin+len(wordBegin)+1
        if posEnd>posBegin:
            reading = eliminateNonWordChar(page[posBegin:posEnd])
            if reading not in readingList:
                readingList.append(reading)
        cursor=posEnd+len(wordEnd)+1
    if readingList == []:
        readingList = ['Not found']
    return jsonify({'status':'success','readingList':readingList}),201

@app.route('/listAllMeaningByWord',methods = ['POST'])
@checkRequestValid(tagList = ['word'])
@checkTimeStamp
def listMeaningByWord():
    meaningList = []
    word = request.json['word'].encode('utf-8')
    req = urllib2.Request(gooURLFront+gooURLMiddleJn2+word+gooURLTail, headers=MozillaFakeHeader)
    page = urllib2.urlopen(req).read()
    pageType = determinePageType(page)
    if pageType == singleResultPage:
        meaningList = parseSingleResultPage(page)
    elif pageType == multipleResultPage:
        meaningList = parseMultipleResultPage(page,word)
    elif pageType == notFoundPage:
        meaningList = ['Not found']
        
    return jsonify({'status':'success','meaningList':meaningList}),201

multipleResultPageKeyword = '国語辞書の検索結果'
NotFoundPageKeyword = '一致する情報は見つかりませんでした'
def determinePageType(page):
    if page.find(NotFoundPageKeyword) != -1:
        return notFoundPage
    result = page.find(multipleResultPageKeyword)
    if result == -1:
        return singleResultPage
    else:
        return multipleResultPage

def filterNoiseBlock(sentence,left,right):
    cursor = sentence.find(left,0)
    while cursor != -1:
        begin = cursor
        end = sentence.find(right,begin)+len(right)
        if end!=-1:
            sentence = sentence.replace(sentence[begin:end],"")
        cursor = sentence.find(left,0)
    return sentence

def getTagText(xml,tagBegin,tagEnd):
    t = tagBegin.find(' ',0)
    if t == -1:
        pureTag=tagBegin
    else:
        pureTag=tagBegin[:t]
    posBegin = xml.find(tagBegin,0)
    if posBegin == -1:
        print 'Cannot find tag : "'+tagBegin+'" in getTagText function'
        return 'error'
    pureTagPos = posBegin
    posEnd = xml.find(tagEnd,posBegin)
    if posEnd == -1:
        print 'cannot find tag : "'+tagEnd+'" in getTagText function'
        return 'error'
    while True:
        pureTagPos = xml.find(pureTag,pureTagPos+len(pureTag),posEnd)
        if pureTagPos == -1:
            break
        else:
            posEnd = xml.find(tagEnd,posEnd+len(tagEnd)) 
    posBegin=posBegin+len(tagBegin)
    return xml[posBegin:posEnd]

def parseSingleResultPage(page):
    cursor = 0
    targetPrevBegin = '<div class="explanation">'
    targetBegin = '<li class="in-ttl-b'
    targetEnd = '</li>'
    exitKeyword = '<!--/explanation-->'
    meaningList = []
    beginPosition = page.find(targetPrevBegin,cursor)
    if beginPosition == 0:
        return []
    endPosition = page.find(exitKeyword,beginPosition)
    page = page[beginPosition:endPosition]
    while cursor != -1:
        posBegin = page.find(targetBegin,cursor)
        if posBegin == -1:
            break
        rawMeaning = getTagText(page[posBegin:],targetBegin,targetEnd)
        posBegin = posBegin + len(rawMeaning)
        if rawMeaning == 'error':
            break
        meaning = filterNoiseBlock(rawMeaning,'<strong>','</strong>')
        meaning = filterNoiseBlock(meaning,'<','>')
        meaning = filterNoiseBlock(meaning,'text','">')
        if meaning[:2]=='">':
            meaning = meaning[2:]
        meaningList.append(meaning)
        cursor = posBegin
    return meaningList

def parseMultipleResultPage(page,word):
    meaningList = []
    targetBegin = 'class="title search-ttl-a">'
    hrefKeywordBegin = 'href="'
    hrefKeywordEnd = '">'
    cursor = 0
    url=''
    while cursor != -1:
        cursor = page.find(targetBegin,cursor)
        if cursor == -1:
            break
        wordBeginPos = page.find(left,cursor)
        wordEndPos = page.find(right,wordBeginPos)
        if wordBeginPos == -1 or wordEndPos == -1:
            break
        if word == page[wordBeginPos+len(left):wordEndPos]:
            startSearchPos = cursor-175
            urlPosBegin = page.find(hrefKeywordBegin,startSearchPos)+len(hrefKeywordBegin)
            urlPosEnd = page.find(hrefKeywordEnd,urlPosBegin)
            if urlPosBegin == -1 or urlPosEnd == -1:
                return meaningList
            urlTail = page[urlPosBegin:urlPosEnd]
            url='http://dictionary.goo.ne.jp'+urlTail
            req = urllib2.Request(url, headers=MozillaFakeHeader)
            concretePage = urllib2.urlopen(req).read()
            meaningList+=parseSingleResultPage(concretePage)
        cursor = wordEndPos
    
    return meaningList

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
