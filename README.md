# CRUD application with FastAPI

## What can this application do?

This application is a REST API application with `FastAPI` framework and it exposes the following endpoints.

| Endpoint      | Method   | Response |
| ------------- | -------- | -------- |
| `/ping`       | `GET`    |          |
| `/notes/{id}` | `GET`    |          |
| `/notes`      | `POST`   |          |
| `/notes/{id}` | `PUT`    |          |
| `/notes/{id}` | `DELETE` |          |

All endponts excepts `GET` method are NOT implemented yet. You can check the endpoints with Docker or Kubernetes.

## TODO

### The application

- [x] The application can communicate with MySQL container
- [ ] The application can accept `POST` request
- [ ] The application can accept `PUT` request
- [ ] The application can accept `DELETE` request
- [ ] Unify the way of logging
- [ ] Introduce ORM

### MySQL

- [x] Launch MySQL container with Kubernetes
- [ ] Create MySQL user when the container is initialized

### Others

- [x] Introduce Argo CD in local
- [ ] Expose Argo CD with service
- [x] Introduce Prometheus
- [x] Introduce Grafana
- [ ] Introduce ELK

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

## Test in local

There are workflows for each tests (unit test and integration test). These workflows are triggered when you create or update a PR based on some conditions.

### Unit test

```bash
> cd src

> green unit_tests -vvv --run-coverage
```

### Integration test

```bash
> docker-compose up -d

> chmod +x check-api-endpoints.sh

> bash check-api-endpoints.sh
```

## Deploy on Kubernetes

You can deploy the application on Kubernetes by manual apply or Argo CD

### Manual deploy

#### Deploy MySQL

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

#### Deploy the application

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

### Deploy the application by Argo CD

The following instructions may work only when you use `minikube` as Kubernetes cluster.

#### Set up Argo CD

```bash
> kubectl apply -f argocd/setup/namespace.yaml
namespace/argocd created

> kubectl get ns | grep argocd
argocd              Active   56s

> kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

> kubectl port-forward svc/argocd-server -n argocd 8080:443
```

You can see the console with `localhost:8080`.

#### Login Argo CD

Get login password by the following command.

```bash
> kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

You can login Argo CD with username `admin` and the password you got.

#### Create a project and an application

```bash
> kubectl create ns database

> kubectl apply -f argocd/projects/database/project.yaml
appproject.argoproj.io/database created

> kubectl apply -f argocd/projects/database/mysql.yaml
application.argoproj.io/database-mysql created

> kubectl create ns api-app

> kubectl apply -f argocd/projects/api-app/project.yaml
appproject.argoproj.io/api-app created

> kubectl apply -f argocd/projects/api-app/fastapi.yaml
application.argoproj.io/api-app-fastapi created
```

#### Check the status of the applications on UI

<img width="1920" alt="貼り付けた画像_2021_04_17_20_33" src="https://user-images.githubusercontent.com/45956169/115111652-45e16700-9fbc-11eb-8f9b-325ca3d02886.png">

## Monitoring

You can monitor the application by Prometheuse. The application expose the endpoint (`/metrics`) for Prometheus. Also, the collected metrics can be shown with Grafana. You can follow the instruction in README in each directory.

## How to update the image?

```bash
> docker login

> docker build src/ -t kanata333/fastapi-example:v<version tag>

> docker push kanata333/fastapi-example:v<version tag>
```
