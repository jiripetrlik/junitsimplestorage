#!/usr/bin/env python3

import connexion
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from database import JunitDatabase
import rest
import argparse
import os

app = connexion.App(__name__, specification_dir='./')

@app.route('/')
def hello():
    statistics = {
        "numberOfTestRuns" : rest.junitDatabase.numberOfTestRuns()
    }

    return render_template("index.html", statistics = statistics)

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

    return config

if __name__ == '__main__':
    app.app.config.update(getAppConfig())
    db = SQLAlchemy(app.app)
    rest.junitDatabase = JunitDatabase(db.engine, db.session)
    rest.junitDatabase.createSchema()
    app.add_api('swagger.yml')

    app.run(host='0.0.0.0', port=5000, debug=True)
