FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./requirements.txt

ARG PIP_TRUSTED_HOSTS=""
RUN set -eux; \
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