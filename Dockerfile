FROM python:3.7-stretch

RUN mkdir /src
WORKDIR /src
RUN apt update
RUN apt install postgresql postgresql-contrib
COPY . /src
RUN pip install -r requirements.txt

