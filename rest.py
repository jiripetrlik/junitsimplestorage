import json
import yaml
import connexion
from junit import loadJunitTestRuns
from database import JunitTestRun

junitDatabase = None

def get(page = None, items = None):
    if page == None:
        page = 1
    if items == None:
        items = 100
    
    testRuns = junitDatabase.getTestRuns(page, items)
    testRuns = list(map(lambda t : t.as_dict(), testRuns))

    return testRuns

def import_junit(junit):
    testRuns = loadJunitTestRuns(junit)
    testRunsIds = junitDatabase.insertTestRuns(testRuns)

    result = {
        "numberOfItems" : len(testRunsIds),
        "ids" : testRunsIds
    }
    return result, 201

def query(query):
    contentType = connexion.request.headers["Content-Type"]
    if contentType == "application/json":
        q = json.loads(query)
    elif contentType == "application/yaml":
        q = yaml.loads(query)
    else:
        return "Unsupported content type.", 415
    
    testRuns = junitDatabase.queryTestRuns(q)
    testRuns = list(map(lambda t : t.as_dict(), testRuns))
    return testRuns

def health():
    return "Ready!"
