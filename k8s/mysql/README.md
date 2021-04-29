# How to add a new secret?

```base
kubectl create secret generic mysql-secret -n database --from-literal=<KEY>=<VALUE> --dry-run=client -o yaml > k8s/mysql/overlays/database/secret.yaml
```

```bash
kubeseal -o yaml < k8s/mysql/overlays/database/secret.yaml > k8s/mysql/overlays/database/sealed-secret.yaml
```
