from flask import g
import flask
import pymysql

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = pymysql.connect(
            host = flask.current_app.config['MYSQL_HOST'],
            user = flask.current_app.config['MYSQL_USER'],
            password = flask.current_app.config['MYSQL_PASSWORD'],
            db = flask.current_app.config['MYSQL_DB']
        )
    return db

def executeCommit(sql, args):
    db = get_db()
    with db.cursor() as cursor:
        result = cursor.execute(sql, args)
    db.commit()
    return result

def fetchone(sql, args):
    with get_db().cursor() as cursor:
        cursor.execute(sql, args)
        return cursor.fetchone()

def fetchall(sql, args=()):
    """Fetch all rows from a SQL query."""
    with get_db().cursor() as cursor:
        cursor.execute(sql, args)
        return cursor.fetchall()

    
def fetchall(sql, args=None):
    with get_db().cursor() as cursor:
        cursor.execute(sql, args)
        return cursor.fetchall()
        
    
