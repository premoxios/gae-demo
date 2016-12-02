import logging
from flask import Flask
import random

app = Flask(__name__)

class NotReachableException(Exception) :
    pass

@app.route('/')
def crash():
    # Crash x% of time
    do_crash = True if (random.random() * 10 < 1) else False
    if do_crash:
        _ = 1/0
        raise NotReachableException('The server should have crashed.')
    return 'Did not crash, this time.'

@app.errorhandler(500)
def server_error(e):
    msg = 'An error occurred during a request: %s' % e
    logging.exception(msg)
    return msg, 500