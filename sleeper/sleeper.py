import logging
from flask import Flask
import random
import time

app = Flask(__name__)

@app.route('/')
def mysleep():
    sleep_seconds = round(random.random() * 3, 3)  # sleep 0-3 seconds
    time.sleep(sleep_seconds)
    return 'Slept for %s seconds.' % sleep_seconds

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request: %s' % e)
    return 'An internal error occurred: %s' % e, 500
