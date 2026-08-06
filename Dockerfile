FROM python:3.8-slim

ARG APP_ENV
ENV APP_ENV=${APP_ENV}

COPY . /app
WORKDIR /app

CMD ["python", "hello.py"]