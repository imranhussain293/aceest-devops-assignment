# syntax=docker/dockerfile:1

FROM jenkins/jenkins:lts

USER root

# Install curl + certificates, then install Docker CLI binary
ARG DOCKER_VERSION=26.1.4

# Optional: for environments with TLS interception.
# Preferred: pass CA cert as a BuildKit secret: --secret id=corp_ca,src=corp-ca.crt
# Fallback: set CURL_INSECURE=1 to skip TLS verification (not recommended).
ARG CURL_INSECURE=0

RUN --mount=type=secret,id=corp_ca,required=false \
  set -eux; \
  apt-get update; \
  apt-get install -y --no-install-recommends ca-certificates curl; \
  if [ -f /run/secrets/corp_ca ]; then \
    cp /run/secrets/corp_ca /usr/local/share/ca-certificates/corp_ca.crt; \
    update-ca-certificates; \
  fi; \
  curl_flags="-fsSL"; \
  if [ "${CURL_INSECURE}" = "1" ]; then \
    curl_flags="${curl_flags} -k"; \
  fi; \
  curl ${curl_flags} "https://download.docker.com/linux/static/stable/x86_64/docker-${DOCKER_VERSION}.tgz" -o /tmp/docker.tgz; \
  tar -xzf /tmp/docker.tgz -C /tmp; \
  mv /tmp/docker/docker /usr/local/bin/docker; \
  chmod +x /usr/local/bin/docker; \
  rm -rf /tmp/docker /tmp/docker.tgz; \
  apt-get purge -y --auto-remove curl; \
  rm -rf /var/lib/apt/lists/*

# Optional runtime CA injection (helps Jenkins trust GitHub behind TLS interception)
RUN mkdir -p /certs/ca
COPY jenkins/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

USER jenkins

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]