# Junit Simple Storage

Junit Simple Storage is a database application which
allows users to store test results. It uses relational
databases as a backend.

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