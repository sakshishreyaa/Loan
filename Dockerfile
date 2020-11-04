FROM python:3

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /d

COPY requirements.txt /d

RUN pip install -r requirements.txt

COPY . /d

# FROM node:13.12.0 AS development

# WORKDIR /devfront

# COPY ./frontend/package.json /devfront
# COPY ./frontend/package-lock.json /devfront
# RUN npm install

# COPY ./frontend /devfront
# EXPOSE 3000

# CMD npm start

