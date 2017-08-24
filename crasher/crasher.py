import logging
import random
import time
from flask import Flask

app = Flask(__name__)

class NotReachableException(Exception) :
    pass

@app.route('/')
def crash():
    now = time.localtime()
    bursty_crash(now)
    return random_crash(now)

def bursty_crash(now):
    # Create a burst of errors for 5 minutes every other hour.
    if (now.tm_hour % 2):
        if (now.tm_min< 5):
            if (random.random() < 0.8):
                _ = 1/0
                raise NotReachableException('Server should have crashed.')

def random_crash(now):
    # Deterministically select an error rate based on the current time
    # in minutes. Then crash with that probability.
    random.seed(now.tm_hour*10 + now.tm_min)
    error_rate = random.randint(2, 7) / 100.0
    random.seed()  # Re-seed based on current time
    rnd = random.random()
    if (rnd < error_rate):
        _ = 1/0
        raise NotReadableException('Server shold have crashed.')
    return 'Now: %s, ErrorRate: %f, Random: %.2f' % (now, error_rate, rnd)

@app.errorhandler(500)
def server_error(e):
    msg = 'An error occurred during a request: %s' % e
    logging.exception(msg)
    return msg, 500
