# Prometheus

```bash
> helm version
version.BuildInfo{Version:"v3.5.4", GitCommit:"1b5edb69df3d3a08df77c9902dc17af864ff05d1", GitTreeState:"dirty", GoVersion:"go1.16.3"}

> helm repo add stable https://charts.helm.sh/stable
"stable" already exists with the same configuration, skipping

> helm repo update
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "crossplane-stable" chart repository
...Successfully got an update from the "grafana" chart repository
...Successfully got an update from the "prometheus-community" chart repository
...Successfully got an update from the "bitnami" chart repository
...Successfully got an update from the "stable" chart repository
Update Complete. ⎈Happy Helming!⎈

> helm search repo prometheus-community

> helm install prometheus -n monitoring --create-namespace prometheus-community/prometheus

> kubectl get all -n monitoring
NAME                                                 READY   STATUS    RESTARTS   AGE
pod/prometheus-alertmanager-ccf8f68cd-rnbmd          2/2     Running   0          3m6s
pod/prometheus-kube-state-metrics-685b975bb7-hv2m9   1/1     Running   0          3m6s
pod/prometheus-node-exporter-bgjc2                   1/1     Running   0          3m6s
pod/prometheus-pushgateway-74cb65b858-wbjlr          1/1     Running   0          3m6s
pod/prometheus-server-d9fb67455-g4wqd                2/2     Running   0          3m6s

NAME                                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/prometheus-alertmanager         ClusterIP   10.101.203.45   <none>        80/TCP     3m6s
service/prometheus-kube-state-metrics   ClusterIP   10.98.190.68    <none>        8080/TCP   3m6s
service/prometheus-node-exporter        ClusterIP   None            <none>        9100/TCP   3m6s
service/prometheus-pushgateway          ClusterIP   10.102.21.117   <none>        9091/TCP   3m6s
service/prometheus-server               ClusterIP   10.102.64.214   <none>        80/TCP     3m6s

NAME                                      DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
daemonset.apps/prometheus-node-exporter   1         1         1       1            1           <none>          3m6s

NAME                                            READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/prometheus-alertmanager         1/1     1            1           3m6s
deployment.apps/prometheus-kube-state-metrics   1/1     1            1           3m6s
deployment.apps/prometheus-pushgateway          1/1     1            1           3m6s
deployment.apps/prometheus-server               1/1     1            1           3m6s

NAME                                                       DESIRED   CURRENT   READY   AGE
replicaset.apps/prometheus-alertmanager-ccf8f68cd          1         1         1       3m6s
replicaset.apps/prometheus-kube-state-metrics-685b975bb7   1         1         1       3m6s
replicaset.apps/prometheus-pushgateway-74cb65b858          1         1         1       3m6s
replicaset.apps/prometheus-server-d9fb67455                1         1         1       3m6s


```
