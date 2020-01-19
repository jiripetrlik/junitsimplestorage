FROM alpine:latest

RUN apk add python3 pcre --no-cache
COPY setup.py docker-files/uwsgi.ini /
COPY junitsimplestorage /junitsimplestorage
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps build-base linux-headers pcre-dev gcc python3-dev musl-dev postgresql-dev && \
 pip3 install --no-cache-dir uwsgi && \
 python3 /setup.py install && \
 apk --purge del .build-deps

EXPOSE 80

CMD ["uwsgi", "/uwsgi.ini"]
