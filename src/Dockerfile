#FROM registry.access.redhat.com/ubi8
#
#WORKDIR /app
#
#COPY Pipfile* /app/
#
### NOTE - rhel enforces user container permissions stronger ##
#USER root
#RUN yum -y install python3
#RUN yum -y install python3-pip wget
#
#RUN pip3 install --upgrade pip \
#  && pip3 install --upgrade pipenv \
#  && pipenv install --system --deploy
#
#USER 1001
#
#COPY . /app
#CMD ["gunicorn", "-b", "0.0.0.0:3000", "--env", "DJANGO_SETTINGS_MODULE=pythondjangoapp.settings.production", "pythondjangoapp.wsgi", "--timeout 120"]

FROM python:3.8-slim-buster

RUN mkdir jett
COPY . /jett/
WORKDIR /jett
RUN apt-get update && apt-get -y install gcc sqlite3 libsqlite3-dev libpq-dev && apt-get clean
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

EXPOSE 8000
ENTRYPOINT [ "python", "-u", "manage.py", "runserver", "0.0.0.0:8000", "--settings=pythondjangoapp.settings.production" ]