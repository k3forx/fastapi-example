# How to add a new secret?

```bash
kubeseal -o yaml < k8s/mysql/overlays/database/secret.yaml > k8s/mysql/overlays/database/sealed-secret.yaml
```
