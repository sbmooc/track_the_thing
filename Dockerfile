FROM tiangolo/uwsgi-nginx:python3.7

RUN apt update
RUN apt install -y postgresql postgresql-contrib
ENV UWSGI_INI tcr_tracker/uwsgi.ini
COPY ./tcr_tracker /tcr_tracker
WORKDIR /tcr_tracker
#RUN pip install -r /track_the_thing/tracker/requirements.txt
