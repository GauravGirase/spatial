# Install Calico (CNI with networkpolicy support)
```bash
kubectcl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.30.2/manifests/calico.yaml
```
### Note: It takes 10-15 min to initialized
## Verify calico installation
```bash
kubectl get daemonset -n kube-system
```
## Step 1: Create Namespace
```bash
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: app-ns
  labels:
    app: app1
```
### set the context with this namespace, so that all the subsequent commands use this namespace
```bash
kubcectl config set-context current --namespace=app-ns
```
## Step 2: Front-end deployment
