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
from DBAccessor import query_db, commit_db_and_get_lastId, commit_db
from SharedFunction import checkRequestValid, checkTimeStamp, getSourceNameTable, generateJsonWord
from flask_cors import cross_origin
import os

app = Flask(__name__)
app.config['DEBUG'] = True

'''This search interface should accept the search target column, but that's too compelx . So if this function want to refactor pls consider the more general way instead of hard coding'''
@app.route('/searchWordByWordAndReading',methods = {'POST'})
@cross_origin()
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
@cross_origin()
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

@app.route('/updateWord',methods = {'POST'})
@cross_origin()
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

@app.route('/deleteWord',methods = {'POST'})
@cross_origin()
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

if __name__ == '__main__':
    app.run(host='0.0.0.0')