# Dockerfile for webhook_handler

FROM python:3.11-slim

ENV WORKDIR=/app
WORKDIR $WORKDIR

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:6000"]
