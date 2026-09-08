# Jfrog oss installation
```bash
https://docs.jfrog.com/installation/docs/docker?_gl=1*g4wvek*_up*MQ..*_ga*MTc5NDI2NzgzOC4xNzg4ODQ0OTI5*_ga_SQ1NR9VTFJ*czE3ODg4NDQ5MjgkbzEkZzAkdDE3ODg4NDQ5MjgkajYwJGwwJGgxMDU2MDc4MzYz
```

# Download sample jar file
```bash
https://www.jgoodies.com/downloads/demos/
```
# Dockerfile with authentication
```bash
FROM eclipse-temurin:21-jre
WORKDIR /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
ARG ARTIFACTORY_URL="http://host.docker.internal:8082"
RUN --mount=type=secret,id=artifactory_user \
    --mount=type=secret,id=artifactory_password \
    curl -fL \
      -u "$(cat /run/secrets/artifactory_user):$(cat /run/secrets/artifactory_password)" \
      "${ARTIFACTORY_URL}/artifactory/devops-maven-local/smart-client-showcase-24.09.0.jar" \
      -o /app/myapp.jar
ENTRYPOINT ["java", "-jar", "/app/myapp.jar"]
```
# Docker BuildKit secrets
```bash
export ARTIFACTORY_USER=admin
export ARTIFACTORY_PASSWORD='YOUR_PASSWORD'
```
### Build
```bash
DOCKER_BUILDKIT=1 docker build \
  --secret id=artifactory_user,env=ARTIFACTORY_USER \
  --secret id=artifactory_password,env=ARTIFACTORY_PASSWORD \
  --build-arg ARTIFACTORY_URL=http://host.docker.internal:8082 \
  -t myapp:1.0 .
```
# If artifactory container runnning on the same EC2 use IP
```bash
hostname -I

# E.G
http://10.0.0.25:8082
```
## Dockerile (without authentication)
```
FROM node:22-bookworm-slim

WORKDIR /app

# Configure npm to use Nexus Repository
RUN npm config set registry \
    http://<IP>:8081/repository/npmjs-proxy/

# Copy package definition first for Docker layer caching
COPY package.json ./

# Install dependencies through Nexus
RUN npm install

# Copy application source
COPY . .

EXPOSE 3000

CMD ["npm", "start"]
```
## Create the secret .npmrc
```bash
cat > nexus-npmrc <<'EOF'
registry=http://13.233.142.196:8081/repository/npmjs-proxy/
//13.233.142.196:8081/repository/npmjs-proxy/:_authToken=YOUR_NEXUS_TOKEN
always-auth=true
EOF
```
```bash
chmod 600 nexus-npmrc
```
## Dockerfile with auth
```bash
# syntax=docker/dockerfile:1
FROM node:22-bookworm-slim
WORKDIR /app
COPY package.json ./
# Use Nexus credentials only during this RUN.
# The .npmrc is deleted before the layer is committed.
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm install
EXPOSE 3000
CMD ["npm", "start"]
```
## Build with BuildKit
```bash
DOCKER_BUILDKIT=1 docker build \
  --secret id=npmrc,src=nexus-npmrc \
  -t nexus-npm-test .
```
# Debian based image (without auth)
```
# syntax=docker/dockerfile:1
FROM debian:bookworm-slim
# Configure APT to use Nexus
RUN echo "deb http://13.233.142.196:8081/repository/debian-proxy bookworm main" \
    > /etc/apt/sources.list.d/nexus.list
# Update package metadata through Nexus
RUN apt-get update
# Install real Debian packages through Nexus
RUN apt-get install -y --no-install-recommends \
    curl \
    wget \
    ca-certificates \
    jq \
    git \
    unzip
# Clean APT cache
RUN rm -rf /var/lib/apt/lists/*
CMD ["bash"]
```
# with auth
```bash
# syntax=docker/dockerfile:1

FROM debian:bookworm-slim

ARG NEXUS_HOST=13.233.142.196:8081
ARG NEXUS_REPO=debian-proxy

# Configure Nexus repository
RUN echo "deb http://${NEXUS_HOST}/repository/${NEXUS_REPO} bookworm main" \
    > /etc/apt/sources.list.d/nexus.list

# Use Nexus credentials only during this build step
RUN --mount=type=secret,id=apt_auth,target=/run/secrets/apt_auth \
    set -eux; \
    auth="$(cat /run/secrets/apt_auth)"; \
    printf 'machine %s login %s password %s\n' \
        "${NEXUS_HOST}" \
        "${auth%%:*}" \
        "${auth#*:}" \
        > /etc/apt/auth.conf; \
    chmod 600 /etc/apt/auth.conf; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        curl \
        wget \
        ca-certificates \
        jq \
        git \
        unzip; \
    rm -rf /var/lib/apt/lists/* /etc/apt/auth.conf
```
