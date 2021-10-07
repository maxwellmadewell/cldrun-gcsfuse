# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.9

# Allow statements and log messages to immediately appear in the Cloud Run logs
ENV PYTHONUNBUFFERED True

# Copy application dependency manifests to the container image.
# Copying this separately prevents re-running pip install on every code change.
COPY requirements.txt ./

# Install production dependencies.
RUN pip install -r requirements.txt
RUN export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s`
RUN echo "deb http://packages.cloud.google.com/apt gcsfuse-buster main" | tee /etc/apt/sources.list.d/gcsfuse.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
RUN apt-get update
RUN apt-get install -y apt-utils kmod
RUN apt-get install -y gcsfuse



ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN mkdir -p /app/input
RUN mkdir -p /app/output

RUN chmod +x /app/main.py

#PORT env variable assigned by gcloud
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app