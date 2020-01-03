import connexion
from flask_sqlalchemy import SQLAlchemy
import os
import datetime

def create_app(config={}):
    app = connexion.App(__name__, specification_dir='./')
    from junitsimplestorage.database import JunitDatabase
    import junitsimplestorage.rest as rest
    import junitsimplestorage.gui as gui

    finalConfig = getAppConfig()
    finalConfig.update(config)
    app.app.config.update(finalConfig)
    db = SQLAlchemy(app.app)
    junitDatabase = JunitDatabase(db.engine, db.session)
    junitDatabase.createSchema()
    rest.junitDatabase = junitDatabase
    gui.junitDatabase = junitDatabase
    app.add_api('swagger.yml')
    app.app.register_blueprint(gui.bp)

    return app.app

def getAppConfig():
    # Default config
    config = {
        "SQLALCHEMY_DATABASE_URI" : "sqlite:///" + os.getcwd() + "/test.db",
        "SQLALCHEMY_ECHO" : False,
        "SECRET_KEY" : os.urandom(24)
    }

    # Read configuration from environment variables
    environmentVariables = ["SQLALCHEMY_DATABASE_URI", "SQLALCHEMY_ECHO"]
    for variable in environmentVariables:
        if (variable in os.environ) and (len(os.environ[variable]) > 0):
            config[variable] = os.environ[variable]
    
    return config