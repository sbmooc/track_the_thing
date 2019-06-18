FROM python:3.7-stretch

RUN mkdir /src
WORKDIR /src

COPY . /src 

RUN pip install -r requirements.txt

