# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify
from flask import abort
import urllib.request
from urllib.parse import quote
import sqlite3
from random import randint
import time
from functools import wraps
from flask import url_for, redirect, render_template
from DBAccessor import query_db, commit_db_and_get_lastId, commit_db
from SharedFunction import checkRequestValid, checkTimeStamp
from flask_cors import cross_origin
import os
import logging

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/addSource',methods = {'POST'})
@cross_origin()
@checkRequestValid(tagList = ['username','source'])
@checkTimeStamp
def addSource():
        username = request.json['username']
        sourceName = request.json['source']
        id = commit_db_and_get_lastId('insert into '+username+'_sources' +' (source) values (?)',[sourceName])
        return jsonify({'status':'success','lastId':id}),201

@app.route('/deleteSource',methods = ['POST'])
@cross_origin()
@checkRequestValid(tagList = ['username','sourceId','deleteSourceMode'])
@checkTimeStamp
def deleteSource():
    sourceTableName = request.json['username'] + '_sources'
    wordTableName = request.json['username'] + '_words'
    sourceId = request.json['sourceId']
    deleteSourceMode = request.json['deleteSourceMode']
    
    if deleteSourceMode != '0' and deleteSourceMode != '1':
        print('error deleteSourceMode = '+deleteSourceMode)
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

@app.route('/addWord',methods = {'POST'})
@cross_origin()
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

@app.route('/listSource',methods = {'POST'})
@cross_origin()
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
                     'Content-Type': 'application/json;charset=UTF-8',
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

multipleResultPageKeyword = '国語辞書の検索結果'
NotFoundPageKeyword = '一致する情報は見つかりませんでした'

@app.route('/listAllReadingByWord',methods = ['POST'])
@cross_origin()
@checkRequestValid(tagList = ['word'])
@checkTimeStamp
def listReadingByWord():
    readingList = []
    word = request.json['word'].encode('utf-8')
    wordEnd = left+request.json['word']+right
    wordBegin = '<p class="title">'
    cursor = 0
    url = gooURLFront+gooURLMiddleJn2+quote(word)+gooURLTail
    req = urllib.request.Request(url, headers=MozillaFakeHeader)
    page = urllib.request.urlopen(req).read().decode("utf-8")
    while(cursor!=-1):
        posEnd = page.find(wordEnd,cursor)
        if posEnd==-1:
            break
        posBegin = page.find(wordBegin,posEnd-100)
        posBegin = posBegin+len(wordBegin)
        if posEnd>posBegin and posEnd-posBegin<50:
            reading = eliminateNonWordChar(page[posBegin:posEnd])
            #print(reading)
            if reading not in readingList:
                readingList.append(reading)
        cursor=posEnd+len(wordEnd)+1
    if readingList == []:
        readingList = ['Not found']
    return jsonify({'status':'success','readingList':readingList}),201

@app.route('/listAllMeaningByWord',methods = ['POST'])
@cross_origin()
@checkRequestValid(tagList = ['word'])
@checkTimeStamp
def listMeaningByWord():
    meaningList = []
    word = request.json['word'].encode('utf-8')
    req = urllib.request.Request(gooURLFront+gooURLMiddleJn2+quote(word)+gooURLTail, headers=MozillaFakeHeader)
    page = urllib.request.urlopen(req).read().decode("utf-8")
    pageType = determinePageType(page)
    if pageType == singleResultPage:
        meaningList = parseSingleResultPage(page)
    elif pageType == multipleResultPage:
        meaningList = parseMultipleResultPage(page,word)
    elif pageType == notFoundPage:
        meaningList = ['Not found']
        
    return jsonify({'status':'success','meaningList':meaningList}),201

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
        print('Cannot find tag : "'+tagBegin+'" in getTagText function')
        return 'error'
    pureTagPos = posBegin
    posEnd = xml.find(tagEnd,posBegin)
    if posEnd == -1:
        print('cannot find tag : "'+tagEnd+'" in getTagText function')
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
            req = urllib.request.Request(url, headers=MozillaFakeHeader)
            concretePage = urllib.request.urlopen(req).read()
            meaningList+=parseSingleResultPage(concretePage)
        cursor = wordEndPos
    
    return meaningList

if __name__ == '__main__':
    app.run(host='0.0.0.0')
