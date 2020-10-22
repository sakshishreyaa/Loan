FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /production

ADD . /production

COPY ./requirements.txt /production/requirements.txt

RUN pip install -r requirements.txt

COPY . /production