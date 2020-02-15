# Junit Simple Storage

Junit Simple Storage is a database application which
allows users to store test results. It uses relational
databases as backend.

![screenshot](docs/screenshots/screenshot-list.png)

More screenshots can be found [here](docs/screenshots.md).

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

MySQL: `SQLALCHEMY_DATABASE_URI=mysql+pymysql://user:password@database-url/database-name

Postgres: `SQLALCHEMY_DATABASE_URI=postgresql://user:password@database-url/database-name

## REST API

For more details see OpenAPI specification on `http://localhost:5000/api/ui`

## Docker

Docker image for Junit Simple Storage can be found on
[Docker hub](https://hub.docker.com/r/jiripetrlik/junitsimplestorage).

```
Run docker container with Junit Simple Storage:
docker run -d --name junitsimplestorage -p 8080:80 jiripetrlik/junitsimplestorage

Or with connection to database:
docker run -d --name junitsimplestorage -p 8080:80 -e SQLALCHEMY_DATABASE_URI=postgresql://user:password@database-url/database-name jiripetrlik/junitsimplestorage
```

## Tips

### Import all JUnit results from Maven build using curl

`find -name TEST*xml -exec curl -X POST "http://junitsimplestorage-url:5000/api/import" -H "accept: */*" -H "Content-Type: application/xml" -d "@{}" \;`

or with labels (label1=value1 and label2=value2):

`find -name TEST*xml -exec curl -X POST "http://junitsimplestorage-url:5000/api/import?labels=label1%3Avalue1%2Clabel2%3Avalue2" -H "accept: */*" -H "Content-Type: application/xml" -d "@{}" \;`
