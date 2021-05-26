# CRUD application with FastAPI

## Run in local

You can test the application in your local with docker.

```bash
docker-compose up -d --build
```

After containers successfully run, you can check an endpoint with `curl` command

```bash
curl -s localhost:8000/notes | jq -r
{
  "notes": [
    {
      "id": 1,
      "title": "Beyond the legacy code",
      "description": "Awesome book!"
    },
    {
      "id": 2,
      "title": "Effective Java",
      "description": "Difficult..."
    }
  ]
}
```

You can also access the application with http://localhost:8000/note.

![image](https://user-images.githubusercontent.com/45956169/119678655-a9dc3280-be7a-11eb-9db2-5593fee9b5b7.png)

## Test in local

There are workflows for each tests (unit test and integration test). These workflows are triggered when you create or update a PR based on some conditions.

### Unit test

```bash
cd src

pytest -v --cov --cov-report=term-missing unit_tests/
```

### Integration test

```bash
docker-compose up -d

bash check-api-endpoints.sh
```

## Frontend

### Requirements

```bash
node --version
v16.2.0

npm --version
7.13.0

npm install -g @vue/cli
npm install --save axios

cd front
vue add @vue/router
npm install vuex
```

## Deploy on Kubernetes

You can deploy the application on Kubernetes by manual apply or Argo CD

### Manual deploy

#### Deploy MySQL

First, you need to run MySQL container by statefulset.

```bash
kubectl create ns database

kubectl apply -k k8s/mysql/overlays/database

kubectl get all -n database
```

You can login the database `test` with the following command.

```bash
kubectl exec -it mysql-0 -n database -- mysql -uroot -p$(kubectl get secret -n database  mysql-secret -o yaml | grep MYSQL_ROOT_PASSWORD | sed 's/.*.: \(.*\)/\1/' | base64 --decode) test
```

#### Deploy the application

After, you successfully deploy MySQL container, then you can deploy the application.

```bash
kubectl create ns api-app

kubectl apply -k k8s/fastapi/overlays/api-app/

kubectl get pod -n api-app

kubectl run --restart Never --image curlimages/curl:7.68.0 -it --rm curl sh
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
kubectl apply -f argocd/setup/namespace.yaml

kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

kubectl port-forward svc/argocd-server -n argocd 8080:443
```

You can see the console with `localhost:8080`.

#### Login Argo CD

Get login password by the following command.

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

You can login Argo CD with username `admin` and the password you got.

#### Create a project and an application

```bash
kubectl create ns database

kubectl apply -f argocd/projects/database/project.yaml

kubectl apply -f argocd/projects/database/mysql.yaml

kubectl create ns api-app

kubectl apply -f argocd/projects/api-app/project.yaml

kubectl apply -f argocd/projects/api-app/fastapi.yaml
```

#### Check the status of the applications on UI

<img width="1920" alt="貼り付けた画像_2021_04_17_20_33" src="https://user-images.githubusercontent.com/45956169/115111652-45e16700-9fbc-11eb-8f9b-325ca3d02886.png">

## Monitoring

You can monitor the application by Prometheuse. The application expose the endpoint (`/metrics`) for Prometheus. Also, the collected metrics can be shown with Grafana. You can follow the instruction in README in each directory.

## How to update the image?

```bash
docker login

docker build src/ -t kanata333/fastapi-example:v<version tag>

docker push kanata333/fastapi-example:v<version tag>
```
