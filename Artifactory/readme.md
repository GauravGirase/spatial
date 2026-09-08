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

