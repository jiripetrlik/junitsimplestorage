from flask import Blueprint
from flask import request
from flask import redirect
from flask import render_template
from flask import url_for
from flask import flash
from flask import url_for
from wtforms import Form, StringField, IntegerField, DateField, SelectField, HiddenField, validators
from junitsimplestorage.junit import loadJunitTestRuns

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

@bp.route("/import", methods = ("GET", "POST"))
def importTestRuns():
    if request.method == "POST":
        labelNumber = 1
        labels = {}
        while "label_key_{}".format(labelNumber) in request.form:
            key = request.form["label_key_{}".format(labelNumber)]
            value = request.form["label_value_{}".format(labelNumber)]
            labels[key] = value
            
            labelNumber = labelNumber + 1

        if request.form["type"] == "text":
            testRuns = loadJunitTestRuns(request.form["junit"])
            testRunIds = junitDatabase.insertTestRuns(testRuns, labels)
            flash("{} test runs were created".format(len(testRunIds)))

        if request.form["type"] == "file":
            data = request.files["file"].read()
            testRuns = loadJunitTestRuns(data)
            testRunIds = junitDatabase.insertTestRuns(testRuns, labels)
            flash("{} test runs were created".format(len(testRunIds)))

        return redirect(url_for("gui.importTestRuns"))

    return render_template("import.html")

@bp.route("/query", methods = ["GET"])
def queryTestRuns():
    form = QueryForm(request.args)
    results = None
    prevLink = None
    nextLink = None

    if (len(request.args) > 0) and form.validate():
        arguments = dict(request.args)
        arguments = convertIntParam(arguments, "timeIsLower")
        arguments = convertIntParam(arguments, "timeIsHigher")
        arguments = processDateParam(arguments, "minImportTime")
        arguments = processDateParam(arguments, "maxImportTime")
        arguments = processDateParam(arguments, "minTimeDate")
        arguments = processDateParam(arguments, "maxTimeDate")
        arguments = convertIntParam(arguments, "page")
        print(arguments["state"])
        
        results = junitDatabase.queryTestRuns(arguments)
        
        if results.has_prev:
            url = queryPage(request.args, results.prev_num)
            prevLink = url
        if results.has_next:
            url = queryPage(request.args, results.next_num)
            nextLink = url

    return render_template("query.html", form = form, results = results, prevLink = prevLink, nextLink = nextLink)

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

def convertIntParam(arguments, argumentName):
    arguments = dict(arguments)
    
    if(argumentName in arguments):
        if len(arguments[argumentName]) > 0:
            arguments[argumentName] = int(arguments[argumentName])
        else:
            del arguments[argumentName]

    return arguments

def processDateParam(arguments, argumentName):
    arguments = dict(arguments)

    if(argumentName in arguments):
        if len(arguments[argumentName]) > 0:
            arguments[argumentName] = arguments[argumentName] + " 00:00:00"
        else:
            del arguments[argumentName]
    
    return arguments

def queryPage(params, page):
    params = dict(params)
    params["page"] = page
    url = url_for("gui.queryTestRuns", **params)
    return url

class QueryForm(Form):
    id = IntegerField("Id", validators=[validators.Optional()])
    minImportTime = DateField("Min. import date", validators=[validators.Optional()])
    maxImportTime = DateField("Max. import date", validators=[validators.Optional()])
    minTimeDate = DateField("Min. date", validators=[validators.Optional()])
    maxTimeDate = DateField("Max. date", validators=[validators.Optional()])
    hostname = StringField("Hostname")
    name = StringField("Name")
    classname = StringField("Class name")
    timeIsLower = IntegerField("Time is lower than", validators=[validators.Optional()])
    timeIsHigher = IntegerField("Time is higher than", validators=[validators.Optional()])
    state = SelectField("State", choices=[("", ""), ("passed", "passed"),
        ("skipped", "skipped"), ("failure", "failure"), ("error", "error")])
    message = StringField("Message")
    page = HiddenField("Page")
