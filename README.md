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

You can deploy the application on Kubernetes.

```bash
> kubectl create ns database
namespace/database created

> cd k8s/mysql

> kubectl apply -k overlays/database

```

You can login the database `test` with the following command.

```bash

> kubectl exec -it mysql-0 -n database -- mysql -uroot -p$(kubectl get secret -n database  mysql-secret -o yaml | grep MYSQL_ROOT_PASSWORD | sed 's/.*.: \(.*\)/\1/' | base64 --decode) test

```

TODO
- [x] Prepare a pod for MySQL
- [ ] Enable the application to communicate MySQL container
