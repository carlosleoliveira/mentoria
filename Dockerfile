FROM python:3.12-slim

ARG APP_ENV=development
ARG APP_VERSION=dev
ENV APP_ENV=${APP_ENV} \
    APP_VERSION=${APP_VERSION}

WORKDIR /app
COPY hello.py /app/

CMD ["python", "hello.py"]
