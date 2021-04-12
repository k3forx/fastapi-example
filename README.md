# Example application with FastAPI
## Unit test

```bash

> cd src

> green unit_tests -vvv --run-coverage

```

## Deploy on Kubernetes

TODO
- [ ] Prepare a pod for MySQL

```docker

kubectl apply -f k8s/pod.yaml

```


## Run in local

You can test the applicaion in your local with docker.

```bash

> docker-compose up -d --build

```

After containers successfully run, you can check an endpoint with `curl` command

```bash

> curl localhost:8002/ping
{"ping":"pong!"}%

```
