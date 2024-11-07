from flask import Flask, g
import flask
import pymysql

def initialize_db(app: Flask):
    database = pymysql.connect(
        host = app.config['MYSQL_HOST'],
        user = app.config['MYSQL_USER'],
        password = app.config['MYSQL_PASSWORD'],
        db = app.config['MYSQL_DB']
    )
    with app.app_context():
        g._database = database
        
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
        
def test_db():
    db = get_db()
    with db.cursor() as cursor:
        sql = "SELECT * FROM test"
        cursor.execute(sql)
        return cursor.fetchone()