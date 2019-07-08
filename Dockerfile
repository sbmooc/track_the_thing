FROM tiangolo/uwsgi-nginx:python3.7

RUN apt update
RUN apt install -y postgresql postgresql-contrib
RUN pip install -r app/requirements.txt

