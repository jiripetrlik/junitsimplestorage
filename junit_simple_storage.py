#!/usr/bin/env python3

import connexion
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from database import JunitDatabase
import rest

app = connexion.App(__name__, specification_dir='./')
app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app.app)
rest.junitDatabase = JunitDatabase(db.engine, db.session)
rest.junitDatabase.createSchema()
app.add_api('swagger.yml')

@app.route('/')
def hello():
    statistics = {
        "numberOfTestRuns" : rest.junitDatabase.numberOfTestRuns()
    }

    return render_template("index.html", statistics = statistics)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    