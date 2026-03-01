# Install Calico (CNI with networkpolicy support)
```bash
kubectcl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.30.2/manifests/calico.yaml
```
### Note: It takes 10-15 min to initialize
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
### Set the context with this namespace, so that all the subsequent commands use this namespace
```bash
kubcectl config set-context current --namespace=app-ns
```
## Step 2: Front-end deployment
```bash
# front-end.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-deploy
  namespace: app-ns
spec:
  replicas: 2
  selector:
    matchLabels:
      app: app1
      role: frontend
  template:
    metadata:
      labels:
        app: app1
        role: frontend
   spec:
     containers:
       - name: frontend-container
         image: nginx
         ports:
           - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: frontend-svc
  namespace: app-ns
spec:
  type: NodePort
  selector:
    app: app1
    role: frontend
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
      nodePort: 31000
```
