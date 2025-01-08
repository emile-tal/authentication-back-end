# syntax=docker/dockerfile:1

FROM python:latest
WORKDIR /authentication-back-end

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
ENV FLASK_APP=server
EXPOSE 8080
CMD [ "python3", "server.py"]