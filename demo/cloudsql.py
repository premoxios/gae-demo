import os
import MySQLdb
import random
import time


CLOUDSQL_PROJECT = 'preaton-playground'
CLOUDSQL_INSTANCE = 'us-central1:preaton-playground-gae-db'

def getDb():
    env = os.getenv('SERVER_SOFTWARE')
    if (env and env.startswith('Google App Engine/')):
        # Connect to CloudSQL from App Engine.
        db = MySQLdb.connect(
            unix_socket='/cloudsql/preaton-playground:us-central1:preaton-playground-gae-db',
            user='root',
            passwd='password',
            db='gae_app')
    else:
        # Connect to local mysql.
        db = MySQLdb.connect(
            host='localhost',
            port=3306,
            db='gae_app',
            user='root')
    return db

def db_get():
    db = getDb()
    cursor = db.cursor()
    cursor.execute('SELECT rnd FROM rnd_numbers')
    result = ''
    for query_row in cursor.fetchall():
        result += ' %d' % query_row
    return result

def db_put():
    epoch = time.time()
    rnd = random.randint(0, 100)
    sql = 'insert into rnd_numbers(ts, rnd) values (%d, %d)' % (epoch, rnd)    
    db = getDb()
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    return "Stored random numbers: ts=%d, rnd=%d" % (epoch, rnd)

