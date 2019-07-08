FROM tiangolo/uwsgi-nginx:python3.7

RUN mkdir /app
WORKDIR /app
RUN apt update
RUN apt install -y postgresql postgresql-contrib
COPY . /app
RUN pip install -r requirements.txt

