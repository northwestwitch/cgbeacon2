FROM python:3.8-alpine3.12

MAINTAINER Chiara Rasi

RUN apk update
RUN apk add make automake gcc g++ linux-headers curl libcurl curl-dev \
  zlib-dev bzip2-dev xz-dev libffi-dev curl libressl-dev bash \
  && rm -rf /var/cache/apk/*

COPY requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /app
ADD . /app

RUN pip install -e .
