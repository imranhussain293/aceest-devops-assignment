FROM jenkins/jenkins:lts

USER root

# Install curl + certificates, then install Docker CLI binary
ARG DOCKER_VERSION=26.1.4

RUN apt-get update \
  && apt-get install -y --no-install-recommends ca-certificates curl \
  && curl -fsSL "https://download.docker.com/linux/static/stable/x86_64/docker-${DOCKER_VERSION}.tgz" -o /tmp/docker.tgz \
  && tar -xzf /tmp/docker.tgz -C /tmp \
  && mv /tmp/docker/docker /usr/local/bin/docker \
  && chmod +x /usr/local/bin/docker \
  && rm -rf /tmp/docker /tmp/docker.tgz \
  && apt-get purge -y --auto-remove curl \
  && rm -rf /var/lib/apt/lists/*

USER jenkins