FROM python:3.8-slim

COPY . /app
WORKDIR /app

RUN python hello.py