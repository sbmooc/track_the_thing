FROM matthieugouel/python-gunicorn-nginx:latest
MAINTAINER Matthieu Gouel <matthieu.gouel@gmail.com>

# Copy the application
COPY . /app

# Install application requirements
RUN pip install -U pip
RUN pip install -r /app/requirements.txt