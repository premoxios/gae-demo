# GAE service "loader"
Creates roughly uniform load that varies throughout the day in a diurnal pattern.

To deploy in GAE:
* Deploy the push taskqueue configuration.
  ```
  $ gcloud app deploy queue.yaml
  ```
* Deploy the handlers.
  ```
  $ gcloud app deploy loader.yaml
  ```
* Deploy the cron job to start generating load.
  ```
  $ gcloud app deploy cron.yaml
  ```
