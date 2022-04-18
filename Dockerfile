FROM python:3.8.1

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt-get update && apt-get install -y pipenv

COPY ./Pipfile /code
RUN pipenv install

COPY . /code
RUN pipenv run python manage.py migrate
#RUN mkdir -p /code/static
#RUN pipenv run python manage.py collectstatic --noinput
