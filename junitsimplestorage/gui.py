from flask import Blueprint
from flask import render_template

bp = Blueprint("gui", __name__)
junitDatabase = None

ITEMS_PER_PAGE = 50

@bp.route('/')
def statistic():
    statistics = {
        "numberOfTestRuns" : junitDatabase.numberOfTestRuns(),
        "minImportTime" : showTime(junitDatabase.minImportTime()),
        "maxImportTime" : showTime(junitDatabase.maxImportTime()),
        "minTime" : showNumericValue(junitDatabase.minTime()),
        "maxTime" : showNumericValue(junitDatabase.maxTime())
    }

    return render_template("statistics.html", statistics = statistics)

@bp.route("/list")
@bp.route("/list/<page>")
def list(page = 1):
    page = int(page)
    numberOfTestRuns = junitDatabase.numberOfTestRuns()
    testRuns = junitDatabase.getTestRuns(page, ITEMS_PER_PAGE)

    data = {
        "numberOfTestRuns" : numberOfTestRuns,
        "page" : page,
        "testRuns" : testRuns
    }
    return render_template("list.html", **data)

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
