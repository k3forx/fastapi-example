# Example application with FastAPI

## What can this application do?

This application is a REST API application with `FastAPI` framework and it exposes the following endpoints.

* `/ping`
* `/notes/{id}`

You can check the above endpoints with Docker or Kubernetes.
## TODO
### The application

- [x] The application can communicate with MySQL container
- [ ] The application can accept `POST` request
- [ ] The application can accept `PUT` request
- [ ] The application can accept `DELETE` request
### MySQL

- [x] Launch MySQL container with Kubernetes
- [ ] Create MySQL user when the container is initialized

### Others

- [ ] Introduce Argo CD
- [ ] Introduce Prometheus
- [ ] Introduce Grafana
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

### Deploy MySQL

First, you need to run MySQL container by statefulset.

```bash
> kubectl create ns database
namespace/database created

> kubectl apply -k k8s/mysql/overlays/database
configmap/entrypoint-fgtb28gb95 created
configmap/mycnf-m7dfc72fd9 created
secret/mysql-secret created
service/mysql-headless created
statefulset.apps/mysql created

> kubectl get all -n database
NAME          READY   STATUS    RESTARTS   AGE
pod/mysql-0   1/1     Running   0          33s

NAME                     TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
service/mysql-headless   ClusterIP   None         <none>        3306/TCP   33s

NAME                     READY   AGE
statefulset.apps/mysql   1/1     33s

```

You can login the database `test` with the following command.

```bash

> kubectl exec -it mysql-0 -n database -- mysql -uroot -p$(kubectl get secret -n database  mysql-secret -o yaml | grep MYSQL_ROOT_PASSWORD | sed 's/.*.: \(.*\)/\1/' | base64 --decode) test

```

### Deploy the application

After, you successfully deploy MySQL container, then you can deploy the application.

```bash
> kubectl create ns api-app
namespace/api-app created

> kubectl apply -k k8s/fastapi/overlays/api-app/
configmap/fastapi-configmap-dctbbf26g5 created
secret/fastapi-secret created
service/fastapi created
deployment.apps/fastapi created

> kubectl get pod -n api-app
NAME                       READY   STATUS    RESTARTS   AGE
fastapi-6c4f4bb67f-bvhdp   1/1     Running   0          28s
fastapi-6c4f4bb67f-hq7qq   1/1     Running   0          28s
fastapi-6c4f4bb67f-wbhzp   1/1     Running   0          28s

> kubectl run --restart Never --image curlimages/curl:7.68.0 -it --rm curl sh
If you don't see a command prompt, try pressing enter.
/ $ curl fastapi.api-app.svc.cluster.local:8000/ping
{"ping":"pong!"}/ $ curl fastapi.api-app.svc.cluster.local:8000/notes/1/
{"id":1,"title":"Beyond the legacy code","description":"Awesome book!"}/ $ exit
pod "curl" deleted

```
## How to update the image?

```bash

> docker login

> docker build src/ -t kanata333/fastapi-example:v<version tag>

> docker push kanata333/fastapi-example:v<version tag>

```