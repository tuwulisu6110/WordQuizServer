from flask import jsonify
from flask import request
from flask import abort
from functools import wraps
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