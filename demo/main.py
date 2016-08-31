import logging
from flask import Flask

from cloudsql import db_get, db_put
from form import form, submitted_form, mysleep

def hello():
    return "Hello, World!"

app = Flask(__name__)
app.add_url_rule('/', view_func=hello)
app.add_url_rule('/form', view_func=form)
app.add_url_rule('/submitted_form', view_func=submitted_form, methods=['POST'])
app.add_url_rule('/db_get', view_func=db_get)
app.add_url_rule('/db_put', view_func=db_put)
app.add_url_rule('/sleep', view_func=mysleep)


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request: %s' % e)
    return 'An internal error occurred: %s' % e, 500
