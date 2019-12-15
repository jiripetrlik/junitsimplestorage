import connexion
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import argparse
import os
import datetime

ITEMS_PER_PAGE = 50

def create_app(config={}):
    app = connexion.App(__name__, specification_dir='./')
    from junitsimplestorage.database import JunitDatabase
    import junitsimplestorage.rest as rest

    finalConfig = getAppConfig()
    finalConfig.update(config)
    app.app.config.update(finalConfig)
    db = SQLAlchemy(app.app)
    rest.junitDatabase = JunitDatabase(db.engine, db.session)
    rest.junitDatabase.createSchema()
    app.add_api('swagger.yml')

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

    @app.route("/list")
    @app.route("/list/<page>")
    def list(page = 1):
        numberOfTestRuns = rest.junitDatabase.numberOfTestRuns()
        testRuns = rest.junitDatabase.getTestRuns(page, ITEMS_PER_PAGE)

        data = {
            "numberOfTestRuns" : numberOfTestRuns,
            "page" : page,
            "testRuns" : testRuns
        }
        return render_template("list.html", **data)

    return app.app

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
        "SQLALCHEMY_DATABASE_URI" : "sqlite:///" + os.getcwd() + "/test.db",
        "SQLALCHEMY_ECHO" : False
    }

    # Read configuration from environment variables
    environmentVariables = ["SQLALCHEMY_DATABASE_URI", "SQLALCHEMY_ECHO"]
    for variable in environmentVariables:
        if (variable in os.environ) and (len(os.environ[variable]) > 0):
            config[variable] = os.environ[variable]
    
    return config