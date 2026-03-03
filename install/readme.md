### Docker installation 
```bash
sudo apt-get update
sudo apt-get install ca-certificates curl -y
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add user to docker group (log out / in or newgrp to apply)
sudo usermod -aG docker  ubuntu
newgrp docker
```
### Jenkins installation (with docker cli installed)
Dockerfile
```bash
FROM jenkins/jenkins:2.541.2-jdk21
USER root
RUN apt-get update && apt-get install -y lsb-release ca-certificates curl && \
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc && \
    chmod a+r /etc/apt/keyrings/docker.asc && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
    https://download.docker.com/linux/debian $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable" \
    | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && apt-get install -y docker-ce-cli && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
USER jenkins
RUN jenkins-plugin-cli --plugins "blueocean docker-workflow json-path-api"
```
### Build an image
```bash
docker build -t myjenkins-custom .
```
### Run Jenkins
```bash
docker run \
  --name jenkins-server \
  --restart=on-failure \
  --detach \
  --env DOCKER_HOST=tcp://docker:2376 \
  --env DOCKER_CERT_PATH=/certs/client \
  --env DOCKER_TLS_VERIFY=1 \
  --publish 8080:8080 \
  --publish 50000:50000 \
  --volume jenkins-data:/var/jenkins_home \
  --volume jenkins-docker-certs:/certs/client:ro \
  myjenkins-custom:latest
```
### Access Jenkins 
```bash
http://<SERVER-IP>:8080
```
### Get initialAdmin password
```bash
docker exec -it jenkins-server bash -c "cat /var/jenkins_home/secrets/initialAdminPassword"
```
## Prometheus & Grafana setup
prometheus.yaml
```bash
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - localhost:9093

rule_files:

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets:
          - localhost:9090
        labels:
          app: prometheus
```
### Run prometheus container
```bash
docker run -d \
-p 9090:9090 \
-v /home/ubuntu/prometheus.yml:/etc/prometheus/prometheus.yml \
prom/prometheus:latest
```
### Access prometheus
```bash
http:<SERVER-IP>:9090
```

### Grafana
```bash
docker run -d -p 3000:3000 --name grafana grafana/grafana
```

## InfluxDB
```bash
docker run -d -p 8086:8086 \
  --name influx-db
  --user root
  -v $PWD/data:/var/lib/influxdb \
  influxdb:1.12.2
```
### 
```bash
docker exec -it bbd756954c77 bash
# execute following command
CREATE DATABASE "jenkins" WITH DURATION 365d REPLICATION 1 NAME "jenkins-retention"
SHOW DATABASES;
```

## Install following plgins in jenkins
- InfluxDB
- Job and Stage monitoring
- Prometheus metrics

## Configure influxDB in jenkins


## Update prometheus.yaml
```bash
- job_name: "jenkins"
  metrics_path: '/prometheus'
  static_configs:
    - targets:
        - localhost:8080
```
## Restart prometheus container
```bash
docker restart <prometheus-container>
```


## Queries for dashboard
```bash
- default_jenkins_up{instance="43.205.177.169:8080"}
# Metric: default_jenkins_up 
# Label filter: instance
```
