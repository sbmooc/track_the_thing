FROM tiangolo/uwsgi-nginx:python3.7

RUN apt update
RUN apt install -y postgresql postgresql-contrib
ENV UWSGI_INI /track_the_thing/tracker/uwsgi.ini
COPY ./track_the_thing /track_the_thing
WORKDIR /tracker
RUN pip install -r /track_the_thing/tracker/requirements.txt
