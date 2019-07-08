FROM tiangolo/uwsgi-nginx:python3.7

RUN apt update
RUN apt install -y postgresql postgresql-contrib
ENV UWSGI_INI tracker/uwsgi.ini
COPY ./tracker /tracker
WORKDIR /tracker
#RUN pip install -r /track_the_thing/tracker/requirements.txt
