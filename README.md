# Example application with FastAPI
## Run in local

You can test the applicaion in your local with docker.

```bash

> docker-compose up -d --build

```

After containers successfully run, you can check an endpoint with `curl` command

```bash

> curl localhost:8002/ping
{"ping":"pong!"}%

> curl localhost:8002/notes/1/
{"id":1,"title":"Beyond the legacy code","description":"Awesome book!"}%

> curl localhost:8002/notes/2/
{"detail":"Note not found"}%

```
## Unit test

```bash

> cd src

> green unit_tests -vvv --run-coverage

```

## Deploy on Kubernetes

TODO
- [ ] Prepare a pod for MySQL
