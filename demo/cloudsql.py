import logging
import os
import pymysql
import random
import sqlalchemy
import time

CLOUDSQL_PROJECT = 'preaton-playground'
CLOUDSQL_INSTANCE = 'us-central1:preaton-playground-gae-db'

def getDb():
    env = os.getenv('GAE_ENV', '')
    prod_env = env.startswith('standard')
    print('Using production environment: %s (%s)' % (prod_env, env))

    if (prod_env):
        db = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL.create(
                drivername="mysql+pymysql",
                username='root',
                password='password',
                database='gae_app',
                query={
                    'unix_socket': '/cloudsql/preaton-playground:us-central1:preaton-playground-gae-db'
                    }
                ))
    else:
        # Connect to local mysql.
        db = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL.create(
                drivername="mysql+pymysql",
                username='root',
                password='password',
                database='gae_app',
                host='localhost',
                port=3306))
    return db

def db_get():
    engine = getDb()
    with engine.connect() as connection:
        sql_cmd = 'SELECT rnd FROM rnd_numbers'
        sql_result = connection.execute(sql_cmd)
        response = 'Random numbers:'
        for row in sql_result:
            response += ' %s' % row
    return response

def db_put():
    epoch = time.time()
    rnd = random.randint(0, 100)
    sql_cmd = 'INSERT INTO rnd_numbers(ts, rnd) VALUES (%d, %d)' % (epoch, rnd)    

    engine = getDb()
    with engine.connect() as connection:
        sql_result = connection.execute(sql_cmd)
    return "Stored random numbers: ts=%d, rnd=%d" % (epoch, rnd)

