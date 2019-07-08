FROM tiangolo/uwsgi-nginx:python3.7

RUN apt update
RUN apt install -y postgresql postgresql-contrib
ENV UWSGI_INI tcr_tracker/uwsgi.ini
COPY . /tracker
WORKDIR /tracker
RUN pip install -r requirements.txt
