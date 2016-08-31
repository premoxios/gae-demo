from flask import render_template, request
from google.appengine.api import urlfetch
import os
import random

def form():
    return render_template('form.html')

def submitted_form():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']

    return render_template(
        'submitted_form.html',
        name=name,
        email=email,
        site=site,
        comments=comments)

def mysleep():
    env = os.getenv('SERVER_SOFTWARE')
    if (env and env.startswith('Google App Engine/')):
        sleeper_url = os.environ.get('SLEEPER_SERVICE_URL')
    else:
        sleeper_url = os.environ.get('LOCAL_SLEEPER_SERVICE_URL')

    rpcs = []
    for _ in range(0, random.randint(1, 5)):
        sleep_rpc = urlfetch.create_rpc()
        urlfetch.make_fetch_call(sleep_rpc, sleeper_url)
        rpcs.append(sleep_rpc) 

    response = '<p>Issued %d calls.</p>' % len(rpcs)
    response += '<ol>'
    for rpc in rpcs:
        rpc.wait()
        
        try:
            result = rpc.get_result()
            if result.status_code == 200:
                response += '<li>Sleep success! : %s</li>' % result.content
            else:
                response += '<li>Sleep failed: %s</li>' % result.status_code
        except Exception as e:
            return "Exception: %s" % e
    response += '</ol>'

    return response
