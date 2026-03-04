FROM python:3.12-alpine

LABEL maintainer="gauravgirase1996@gmail.com" \
      org.opencontainers.image.title="Homepage service" \
      org.opencontainers.image.description="Homepage service for ingress poc" \
      org.opencontainers.image.version="v1.0.0"

WORKDIR /app

RUN addgroup -S python-group \
    && adduser -S python-user -G python-group

COPY --chown=python-user:python-group application/ /app

USER python-user

EXPOSE 5678

CMD ["python3", "-m", "http.server", "5678", "--bind", "0.0.0.0"]
      
