#!/usr/bin/env python3

import connexion
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from database import JunitDatabase
import rest
import argparse
import os
import datetime

app = connexion.App(__name__, specification_dir='./')

@app.route('/')
def statistic():
    statistics = {
        "numberOfTestRuns" : rest.junitDatabase.numberOfTestRuns(),
        "minImportTime" : showTime(rest.junitDatabase.minImportTime()),
        "maxImportTime" : showTime(rest.junitDatabase.maxImportTime()),
        "minTime" : showNumericValue(rest.junitDatabase.minTime()),
        "maxTime" : showNumericValue(rest.junitDatabase.maxTime())
    }

    return render_template("statistics.html", statistics = statistics)

def showNumericValue(variable):
    if variable == None:
        return "-"
    else:
        return round(variable, 2)

def showTime(variable):
    if variable == None:
        return "-"
    else:
        return variable.strftime("%Y-%m-%d %H:%M:%S")

def getAppConfig():
    # Default config
    config = {
        "SQLALCHEMY_DATABASE_URI" : "sqlite:///test.db",
        "SQLALCHEMY_ECHO" : False
    }

    # Read configuration from environment variables
    environmentVariables = ["SQLALCHEMY_DATABASE_URI", "SQLALCHEMY_ECHO"]
    for variable in environmentVariables:
        if (variable in os.environ) and (len(os.environ[variable]) > 0):
            config[variable] = os.environ[variable]

    # Read configuration from commad line arguments
    parser = argparse.ArgumentParser(description = "JUnit Simple Storage")
    parser.add_argument("-d", "--database", required=False, help="SQL database URI", type=str)
    parser.add_argument("-e", "--echo-sql", action="store_true", required=False, help="Echo SQL queries")
    args = parser.parse_args()
    if args.database != None:
        config["SQLALCHEMY_DATABASE_URI"] = args.database
    if args.echo_sql == True:
        config["SQLALCHEMY_ECHO"] = args.echo_sql
    
    return config

if __name__ == '__main__':
    app.app.config.update(getAppConfig())
    db = SQLAlchemy(app.app)
    rest.junitDatabase = JunitDatabase(db.engine, db.session)
    rest.junitDatabase.createSchema()
    app.add_api('swagger.yml')

    app.run(host='0.0.0.0', port=5000, debug=True)
