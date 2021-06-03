import os
import random
import requests

def getEnvForDeployment(envvar):
    env = os.getenv('SERVER_SOFTWARE')
    if (env and env.startswith('Google App Engine/')):
        return os.environ.get(envvar)
    return os.environ.get('LOCAL_%s' % envvar)
  
def mysleep():
    sleeper_url = getEnvForDeployment('SLEEPER_SERVICE_URL')

    # Create several async requests to the sleeper service.
    responses = []
    with requests.session() as session:
        for _ in range(0, random.randint(1, 5)):
            responses.append(session.get(sleeper_url))

    response = '<p>Issued %d calls.</p>' % len(responses)
    response += '<ol>'
    for r in responses:
        # Block until the async request completes
        rc = r.status_code
        
        try:
            if rc == 200:
                response += '<li>Sleep success! : %s</li>' % r.text
            else:
                response += '<li>Sleep failed: %s</li>' % rc
        except Exception as e:
            return "Exception: %s" % e
    response += '</ol>'

    return response

def crash():
    crash_url = getEnvForDeployment('CRASH_SERVICE_URL')
    response = requests.get(crash_url)
    try:
        if response.status_code == 200:
            return 'Did not crash.'
        else:
            return 'Crashed!'
    except Exception as e:
        return 'Exception: %s' % e
