# clinician-availability

## Prerequisite
* Docker w/ Docker Compose

## Build
  ```
  git clone https://github.com/bluedenim/clinician-availability.git
  cd clinician-availability
  docker-compose build
  ```

## Run
```
docker-compose up app
```

## API Endpoint
* http://localhost:8000/availabilities?format=json -- API endpoint. Optional params:
  * **datetime**: ISO 8601 formatted start date/time (e.g. `2022-01-01T12:00:00Z`). Default is **now**.
  * **days_ahead**: number of days into the future from datetime to include when getting availabilities. Default is **10**. Max is **100**.
  * The endpoint will take upwards to 8 seconds to return
  * The endpoint will have a 15% chance to throw a 500 error

## Unit test
To run tests:
```
docker-compose run --rm app pipenv run pytest
```
