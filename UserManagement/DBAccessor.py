import sqlite3
from random import randint
DATABASE = '/Database/wordQuizData.db'
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