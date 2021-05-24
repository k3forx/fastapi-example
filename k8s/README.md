# Prometheus Operator

Prometheus, alertmanager, and pushgeteway can be managed by Prometheus operator.

## Deploy

```bash
kubectl apply -f argocd/namespaces/monitoring.yaml

kubectl apply -f argocd/projects/monitoring/project.yaml

kubectl apply -f argocd/projects/monitoring/prometheus-operator.yaml
```

With Argo CD, Prometheus is automatically deployed.

## Visualize metric by Prometheus UI

At first, you need to expose service with `minikube service` command.

```bash
minikube service -n monitoring prometheus --url
```

You can get URL of Prometheus UI and visualize metrics of applications with PromQL. The following queries are examples.

- The number of 4xx errors in 5 mins: `sum(increase(fastapi_requests_total{status_code=~"4[0-9]+", path="/notes/{note_id}"}[5m]))`

## Visualize metrics by Grafana

### Add a new datasource

- prometheus.monitoring.svc.cluster.local:9090

# Prometheus

With prometheus and Grafana and alert manager, you can monitor the application.

## Set up Promtheus

If you use minikube as Kubernetes cluster, you need to launch it with the following parameters so that prometheuse-server can collect metrics of the application.

```bash
minikube start --extra-config=kubelet.authentication-token-webhook=true --extra-config=kubelet.authorization-mode=Webhook
```

## Deploy

You can deploy Prometheus manually or use Argo CD. Before you deploy it, you need to create namaspace `monitoring` beforehand.

```bash
kubectl create ns monitoring
```

### Deploy by manual

### Deploy by Argo CD

You can also use Argo CD to deploy Prometheus.

```bash
kubectl apply -f argocd/projects/monitoring/project.yaml

kubectl apply -f argocd/projects/monitoring/prometheus.yaml
```

## Check the status of applications

You can check the status of the application by `kubectl` command or Argo CD UI.

```bash
kubectl get all -n monitoring
NAME                              READY   STATUS    RESTARTS   AGE
pod/prometheus-575865f89f-rkc4v   1/1     Running   0          31m

NAME                 TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
service/prometheus   NodePort   10.100.39.170   <none>        9090:31919/TCP   34m

NAME                         READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/prometheus   1/1     1            1           31m

NAME                                    DESIRED   CURRENT   READY   AGE
replicaset.apps/prometheus-575865f89f   1         1         1       31m
```

Argo CD

<img width="1920" alt="貼り付けた画像_2021_04_17_20_35" src="https://user-images.githubusercontent.com/45956169/115111709-86d97b80-9fbc-11eb-928c-4ee4789255ff.png">

## Open prometheus UI

The type of the service for prometheus-server is `NodePort`. Then you can open the console of prometheus with the following command.

```bash
minikube service prometheus -n monitoring --url
```

You can visit the console with the above URL you got.

![image](https://user-images.githubusercontent.com/45956169/115111489-973d2680-9fbb-11eb-90cc-fc895d407c86.png)

Also, you can check that Prometheus can pull metrics from the application on the UI.

![image](https://user-images.githubusercontent.com/45956169/115111520-c05db700-9fbb-11eb-8c86-acc58e4c28d6.png)

## Deploy Alert Manager

After you confirm that Prometheus can collect the metrics, you can set alerts based on the changes of the status of the application.

By default, the following alert is set.

```YAML
apiVersion: v1
kind: ConfigMap
metadata:
  name: alertmanager-config
data:
  alertmanager.yml: |-
    route:
      receiver: 'containers_notification'
    receivers:
    - name: 'containers_notification'
      slack_configs:
        - api_url: '<webhook-url>'
          channel: '<channel name>'
          text: "{{ .CommonAnnotations.summary }}"
          send_resolved: true
```

When the application is down, an alert will be sent to the slack channel with incoming webhook.

You can deploy alert manager with the following command after you update the above YAML file.

```bash
kubectl apply -k k8s/alertmanager/overlays/monitoring
```

## Trigger an alert

```bash
kubectl delete -k k8s/fastapi/overlays/api-app/
```

or

```bash
kubectl delete -f argocd/projects/api-app/fastapi.yaml
```

## Check the slack channel

![image](https://user-images.githubusercontent.com/45956169/115889152-a37b2500-a48e-11eb-9739-75befd1b6c40.png)

## Prometheus Operator

- prometheus operator による prometheus の管理では、kubernetes_sd_config で role に対するサービスディスカバリが実行される。
- その後にラベルセレクタによるターゲットの選定が行われる。
