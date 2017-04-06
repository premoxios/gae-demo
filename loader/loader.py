import logging
from flask import Flask
from google.appengine.api import taskqueue
import math
import random
import time

app = Flask(__name__)

def get_traffic_qps():
    # Compute traffic target in qps. Traffic is diurnal and sinusoidal traffic
    # with minimum traffic at hrs=0.0|24.0 and maximum traffic at hrs=12.0.
    now = time.localtime()
    hrs = now.tm_hour + now.tm_min/60.0
    # Compute scale factor is between 0 and 1.    
    traffic_scaler = -1.0 * math.cos(2.0*math.pi*hrs/24)
    traffic_scaler = (traffic_scaler + 1) / 2.0
    # Scale traffic between peak and trough.
    traffic_trough_qps = 50
    traffic_peak_qps = 100
    traffic_qps = traffic_trough_qps + \
        (traffic_peak_qps-traffic_trough_qps)*traffic_scaler
    # Add jitter of up to 1%.    
    traffic_qps = traffic_qps * (random.uniform(0.99, 1.01))
    return traffic_qps


@app.route("/cron")
def cron():
  # Long-running tasks seem to make cron schedule erratically, so use cron to
  # trigger the long-running task to make traffic. See cron.yaml and queue.yaml.
  task = taskqueue.Task(url="/schedule", target="loader")
  task.add(queue_name="schedule")
  return "OK"


@app.route("/schedule", methods=['POST',])
def schedule():
    # Upon receiving a message from the push taskqueue, generate traffic
    # uniformly for one minute by posting requests to a different push
    # taskqueue (see queue.yaml).
    start = time.time()
    traffic_qps_goal = get_traffic_qps()
    traffic_count_minute_goal =  int(traffic_qps_goal*60)
    print("Creating traffic for one minute: "
          "start=%.3f, qps=%.3f, queries_goal=%d" %
          (start, traffic_qps_goal, traffic_count_minute_goal))

    traffic_count_current = 0
    while True:
        now = time.time()
        traffic_count_goal = int(traffic_qps_goal*(now-start))
        if traffic_count_goal <= traffic_count_current:
            # Sleep until the next request should be sent.
            time.sleep(1.0/traffic_qps_goal)
            continue
        for _ in range(traffic_count_goal-traffic_count_current):
            task = taskqueue.Task(url='/traffic', target='loader')
            task.add(queue_name='traffic')
        traffic_count_current = traffic_count_goal
        if traffic_count_current >= traffic_count_minute_goal:
            break

    end = time.time()
    msg = ("Created traffic for one minute: "
           "time_start=%.3f, time_end=%.3f, interval=%.3f, "
           "qps_goal=%.3f, queries_goal=%d, "
           "qps_actual=%.3f, queries_actual=%d" %
           (start, end, (end-start),
           traffic_qps_goal, traffic_count_minute_goal,
           (traffic_count_current/(end-start)), traffic_count_current)) 
    print msg
    return msg


@app.route('/traffic', methods=['POST',])
def traffic():
  # Generate load with variable response time.
  # Latency=500ms average, 300 ms stddev.
  mu = 500
  sigma = 300
  latency_ms = max(int(random.gauss(mu, sigma)), 10)  # no negative latencies
  time.sleep(latency_ms/1000)
  return "Latency: %d ms" % latency_ms

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during request: %s' % e)
    return 'An internal error occurred: %s' % e, 500
