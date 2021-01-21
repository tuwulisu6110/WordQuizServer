# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify
from flask import abort
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

def generateRandomIdSet(num,maxLimit):
    rIds = []
    while len(rIds)<num:
        r = randint(0,maxLimit)
        while r in rIds:
            r = randint(0,maxLimit)
        rIds.append(r)
    return rIds

@app.route('/randomWord',methods = ['POST'])
@cross_origin()
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
@cross_origin()
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
    


if __name__ == '__main__':
    app.run(host='0.0.0.0',ssl_context=('cert.pem', 'key.pem'))