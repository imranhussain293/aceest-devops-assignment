# syntax=docker/dockerfile:1

FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./requirements.txt

# Optional: support corporate TLS interception during builds.
# - Preferred: pass a CA cert as a BuildKit secret: --secret id=corp_ca,src=corp-ca.crt
# - Fallback: pass trusted hosts (disables TLS verification for those hosts):
#     --build-arg PIP_TRUSTED_HOSTS="pypi.org files.pythonhosted.org"
ARG PIP_TRUSTED_HOSTS=""
RUN --mount=type=secret,id=corp_ca,required=false \
	set -eux; \
	if [ -f /run/secrets/corp_ca ]; then \
		cp /run/secrets/corp_ca /usr/local/share/ca-certificates/corp_ca.crt; \
		update-ca-certificates; \
	fi; \
	pip_args="--no-cache-dir -r ./requirements.txt"; \
	if [ -n "$PIP_TRUSTED_HOSTS" ]; then \
		for host in $PIP_TRUSTED_HOSTS; do \
			pip_args="$pip_args --trusted-host $host"; \
		done; \
	fi; \
	pip install $pip_args

COPY app.py ./app.py
COPY tests ./tests

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "--worker-class", "gthread", "--threads", "4", "--timeout", "120", "app:app"]