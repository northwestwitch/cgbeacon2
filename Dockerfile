FROM python:3.8-alpine3.12

RUN apk update
RUN apk add make automake gcc g++ linux-headers curl libcurl curl-dev \
  zlib-dev bzip2-dev xz-dev libffi-dev curl libressl-dev \
  && rm -rf /var/cache/apk/*

ADD . .

RUN pip install -e . -r requirements.txt

CMD cgbeacon2 run
