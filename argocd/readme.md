## Create k8s secret for docker registry
```bash
kubectl create secret docker-registry dockerhub-secret \
--docker-server=https://index.docker.io/v1 \
--docker-username=gauravgirase \
--docker-password=<ACCESS-TOKEN> \
--docker-email=gaurav.girase111@gmail.com \
--namespace=app1-ns
```
