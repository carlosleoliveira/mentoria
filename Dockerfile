FROM python:3.8-slim

ARG APP_ENV=development

ENV APP_ENV=${APP_ENV}

COPY . /app
WORKDIR /app

RUN python hello.py
