# syntax=docker/dockerfile:1

FROM python:latest
WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
ENV FLASK_APP=server
EXPOSE 8080

CMD ["gunicorn","--config", "gunicorn_config.py", "app:app"]