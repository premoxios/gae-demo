# GAE service "loader"
Creates roughly uniform load that varies throughout the day in a diurnal pattern.

To deploy in GAE:
* Set up queues with the following configuration:
```
$ gcloud tasks queues describe schedule
appEngineRoutingOverride:
  host: loader.preaton-playground.appspot.com
name: projects/preaton-playground/locations/us-central1/queues/schedule
purgeTime: '2021-06-02T18:09:29.939615Z'
rateLimits:
  maxBurstSize: 10
  maxConcurrentDispatches: 1000
  maxDispatchesPerSecond: 5.0
retryConfig:
  maxAttempts: -1
  maxBackoff: 3600s
  maxDoublings: 16
  minBackoff: 0.100s
stackdriverLoggingConfig:
  samplingRatio: 1.0
state: RUNNING

$ gcloud tasks queues describe traffic
appEngineRoutingOverride:
  host: loader.preaton-playground.appspot.com
name: projects/preaton-playground/locations/us-central1/queues/traffic
purgeTime: '2021-06-02T20:35:08.875988Z'
rateLimits:
  maxBurstSize: 100
  maxConcurrentDispatches: 1000
  maxDispatchesPerSecond: 500.0
retryConfig:
  maxAttempts: 10
  maxBackoff: 3600s
  maxDoublings: 16
  minBackoff: 0.100s
stackdriverLoggingConfig:
  samplingRatio: 1.0
state: RUNNING
```
* Deploy the handlers.
  ```
  $ gcloud app deploy loader.yaml
  ```
* Deploy the cron job to start generating load.
  ```
  $ gcloud app deploy cron.yaml
  ```
