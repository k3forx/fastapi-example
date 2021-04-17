# Prometheus

With prometheus and Grafana, you can monitor the application.

## Set up Promtheus

If you use minikube as Kubernetes cluster, you need to launch it with the following parameters so that prometheuse-server can collect metrics of the application.

```bash
> minikube start --extra-config=kubelet.authentication-token-webhook=true --extra-config=kubelet.authorization-mode=Webhook
```

## Deploy

You can deploy Prometheus manually or use Argo CD. Before you deploy it, you need to create namaspace `monitoring` beforehand.

```bash
> kubectl create ns monitoring
```

### Deploy by manual

### Deploy by Argo CD

You can also use Argo CD to deploy Prometheus.

```bash
> kubectl apply -f argocd/projects/monitoring/project.yaml

> kubectl apply -f argocd/projects/monitoring/prometheus.yaml
```

## Check the status of applications

You can check the status of the application by `kubectl` command or Argo CD UI.

```bash
> kubectl get all -n monitoring
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
> minikube service prometheus -n monitoring --url
```

You can visit the console with the above URL you got.

![image](https://user-images.githubusercontent.com/45956169/115111489-973d2680-9fbb-11eb-90cc-fc895d407c86.png)

Also, you can check that Prometheus can pull metrics from the application on the UI.

![image](https://user-images.githubusercontent.com/45956169/115111520-c05db700-9fbb-11eb-8c86-acc58e4c28d6.png)
