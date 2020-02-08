FROM alpine:latest

RUN apk add python3 pcre --no-cache
COPY setup.py docker-files/uwsgi.ini /
COPY junitsimplestorage /junitsimplestorage
RUN \
 apk add --no-cache postgresql-libs libffi && \
 apk add --no-cache --virtual .build-deps build-base linux-headers pcre-dev gcc python3-dev musl-dev postgresql-dev libffi-dev && \
 pip3 install --no-cache-dir uwsgi psycopg2-binary PyMySQL cryptography && \
 python3 /setup.py install && \
 apk --purge del .build-deps

ENV SQLALCHEMY_DATABASE_URI sqlite:////data/junit-simple-storage.db

VOLUME [ "/data" ]
EXPOSE 80

CMD ["uwsgi", "/uwsgi.ini"]
