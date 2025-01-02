# syntax=docker/dockerfile:1

FROM python:latest
WORKDIR /authentication-back-end

# Install dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Run table migrations in postgres
# COPY run_migrations.py .
# RUN python3 run_migrations.py

COPY . .
ENV FLASK_APP=server
EXPOSE 5000
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]