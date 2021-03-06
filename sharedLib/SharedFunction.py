from flask import jsonify
from flask import request
from flask import abort
from functools import wraps
from DBAccessor import query_db, commit_db_and_get_lastId, commit_db
import time
def checkRequestValid(tagList=[]):
    def decorator_checkRequestValid(func):
        @wraps(func)
        def func_checkRequestValid():
            if not request.json:
                abort(400)
            for tag in tagList:
                if not tag in request.json:
                    print('no tag : ' + tag)
                    return jsonify({'status':'lost params : '+tag}),399
                if request.json[tag] is None:
                    print('request['+tag+'] is null')
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
def getSourceNameTable(sourceTableName):
    sourceNameRows = query_db('select * from '+sourceTableName)
    sourceNameTable = {-1:''}
    '''this is for the condition that no sourceName in some words'''
    if sourceNameRows is not None:
        for snRow in sourceNameRows:
            sourceNameTable[snRow['id']] = snRow['source']
    return sourceNameTable
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