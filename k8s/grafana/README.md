# Grafana

Grafana is used to visualize metrics that are collected by Prometheus.

## Deploy Grafana

You can deploy Grafana by Argo CD.

```bash
> kubectl create ns monitoring

> kubectl apply -f argocd/projects/monitoring/project.yaml

> kubectl apply -f argocd/projects/monitoring/grafana.yaml
```

## Check Grafana on UI

You can get the login url for Grafana by the following command.

```bash
> minikube service -n monitoring grafana --url
```

![image](https://user-images.githubusercontent.com/45956169/115117311-d463e180-9fd8-11eb-9d94-72624325cf4b.png)

## Examples of metrics

- `starlette_requests_total{path!="/metrics"}`

References:

- https://prometheus.io/docs/prometheus/latest/querying/basics/
