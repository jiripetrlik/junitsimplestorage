# Junit Simple Storage

Junit Simple Storage is a database application which
allows users to store test results. It uses relational
databases as a backend.

![screenshot](docs/screenshots/screenshot.png)

## Install

Use `setup.py` in the project parent directory to install
Junit Simple storage `python setup.py install`.

## Run

```
export FLASK_APP=junitsimplestorage
flask run
```

It is possible to access the running application on `http://localhost:5000`

## Environment properties

`SQLALCHEMY_DATABASE_URI` ... Connection string for database

### Examples of database connection strings

MySQL: `SQLALCHEMY_DATABASE_URI=mysql+pymysql://user:password@mysql/junitsimplestorage junitsimplestorage`

Postgres: `SQLALCHEMY_DATABASE_URI=postgresql://user:password@postgres/junitsimplestorage junitsimplestorage`

## REST API

For more details see OpenAPI specification on `http://localhost:5000/api/ui`

## Docker

Docker image for Junit Simple Storage can be found on
[Docker hub](https://hub.docker.com/r/jiripetrlik/junitsimplestorage).

```
Run docker container with Junit Simple Storage:
docker run -d --name junitsimplestorage -p 8080:80 jiripetrlik/junitsimplestorage

Or with connection to database:
docker run -d --name junitsimplestorage -p 8080:80 -e SQLALCHEMY_DATABASE_URI=postgresql://user:password@postgres/junitsimplestorage jiripetrlik/junitsimplestorage
```
