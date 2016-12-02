import logging
from flask import Flask
import random

app = Flask(__name__)

class NotReachableException(Exception) :
    pass

@app.route('/')
def crash():
    start = int(random.random() * 10) + 10
    end = start + int(random.random() * 10) + 1
    x = [int(x*random.random()) for x in range(start, end)]
    logging.info('Input: %s' % x)
    return check_for_crash(x, 0)

def check_for_crash(x, i):
    if (len(x) <= i):
      return 'EOF'
    do_crash = True if (x[i] == i) else False
    if do_crash:
      _ = 1/0
      raise NotReachableException('The server should have crashed.')
    msg = check_for_crash(x, i+1)
    return '%d/%d, %s' % (i, x[i], msg)

@app.errorhandler(500)
def server_error(e):
    msg = 'An error occurred during a request: %s' % e
    logging.exception(msg)
    return msg, 500