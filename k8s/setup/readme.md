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
## Step 2: Front-end resources deployment
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
## Step 3: Backend resources deployment
```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-deploy
  namespace: app-ns
spec:
  replicas: 2
  selector:
    matchLabels:
      app: app1
      role: backend
  template:
    metadata:
      labels:
        app: app1
        role: backend
    spec:
      containers:
        - name: backend-container
          image: python:3.12-slim
          command: ["python3", "-m", "http.server", "5678"]
          ports:
            - containerPort: 5678
---
apiVersion: v1
kind: Service
metadata:
  name: backend-server
  namespace: app-ns
spec:
  type: ClusterIP
  selector:
    app: app1
    role: backend
  ports:
    - protocol: TCP
      port: 5678
      targetPort: 5678
  ```
## Step 4: Database deployment using statefulset
```bash
apiVersion: v1
kind: Service
metadata:
  name: db-svc
  namespace: app-ns
spec:
  clusterIP: None
  selector:
    app: app1
    role: db
  ports:
    - protocol: TCP
      port: 3306
      targetPort: 3306
---
apiVersion: apps/v1
kind: Stateful
metadata:
  name: db-sts
  namespace: app-ns
spec:
  serviceName: db-svc
  replicas: 1
  selector:
    matchLabels:
      app: app1
      role: db
  spec:
    containers:
      - name: mysql-container
        image: mysql:8.0
        ports:
          - containerPort: 3306
        env:
          - name: MYSQL_ROOT_PASSWORD
            value: "mystrongpassword"
```
## Test: without network policies
- Check communication from frontend pod
```bash
kubectl exec -it frontend-deploy-abc12344 -- bash
# install telnet
apt update && apt install -y telnet
telent backend-svc 5678
o/p: Connected to backend-svc
telent db-svc 3306
o/p: Connected to backend-svc
```

