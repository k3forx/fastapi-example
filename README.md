# Example application with FastAPI

How to run the application in local

```bash

> docker-compose up -d --build

```

After containers successfully run, you can check an endpoint with `curl` command

```bash

> curl localhost:8002/ping
{"ping":"pong!"}%

```

# Unit test

```bash

> cd src

> green unit_tests -vvv --run-coverage

```

# Deploy on Kubernetes

TODO
- [ ] Prepare a pod for MySQL

```docker

kubectl apply -f k8s/pod.yaml

```
