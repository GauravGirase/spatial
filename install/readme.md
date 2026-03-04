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
## Node exporter installation
```bash
wget https://github.com/prometheus/node_exporter/releases/download/v1.10.2/node_exporter-1.10.2.linux-amd64.tar.gz
tar xvfz node_exporter-1.10.2.linux-amd64.tar.gz
cd node_exporter-1.10.2.linux-amd64
./node_exporter
```
## AWS CLI installation
```bash
sudo apt install unzip
curl -fsSL https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip -o /tmp/awscliv2.zip
unzip -q /tmp/awscliv2.zip -d /tmp
/tmp/aws/install
aws --version
```
## Kubectl installation
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
# Note:
# If you do not have root access on the target system, you can still install kubectl to the ~/.local/bin directory:
chmod +x kubectl
mkdir -p ~/.local/bin
mv ./kubectl ~/.local/bin/kubectl
# and then append (or prepend) ~/.local/bin to $PATH
kubectl version --client
```
## eksctl installation (https://docs.aws.amazon.com/eks/latest/eksctl/installation.html#_for_unix)
```bash
# for ARM systems, set ARCH to: `arm64`, `armv6` or `armv7`
ARCH=amd64
PLATFORM=$(uname -s)_$ARCH

curl -sLO "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_$PLATFORM.tar.gz"

# (Optional) Verify checksum
curl -sL "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_checksums.txt" | grep $PLATFORM | sha256sum --check

tar -xzf eksctl_$PLATFORM.tar.gz -C /tmp && rm eksctl_$PLATFORM.tar.gz

sudo install -m 0755 /tmp/eksctl /usr/local/bin && rm /tmp/eksctl
```
