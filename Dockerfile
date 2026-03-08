FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

COPY app.py ./app.py
COPY tests ./tests

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "--worker-class", "gthread", "--threads", "4", "--timeout", "120", "app:app"]