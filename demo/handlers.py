import os
import random
from google.appengine.api import urlfetch

def getEnvForDeployment(envvar):
    env = os.getenv('SERVER_SOFTWARE')
    if (env and env.startswith('Google App Engine/')):
        return os.environ.get(envvar)
    return os.environ.get('LOCAL_%s' % envvar)
  
def mysleep():
    sleeper_url = getEnvForDeployment('SLEEPER_SERVICE_URL')
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

def crash():
    crash_url = getEnvForDeployment('CRASH_SERVICE_URL')
    crash_rpc = urlfetch.create_rpc()
    urlfetch.make_fetch_call(crash_rpc, crash_url)
    crash_rpc.wait()
    try:
        result = crash_rpc.get_result()
        if result.status_code == 200:
            return 'Did not crash.'
        else:
            return 'Crashed!'
    except Exception as e:
        return 'Exception: %s' % e