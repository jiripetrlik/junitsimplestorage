import json
import yaml
import connexion
from junitsimplestorage.junit import loadJunitTestRuns
from junitsimplestorage.database import JunitTestRun

junitDatabase = None

def get(page = None, items = None):
    if page == None:
        page = 1
    if items == None:
        items = 100
    
    testRuns = junitDatabase.getTestRuns(page, items).items

    return marshallTestRuns(testRuns)

def import_junit(body, labels = None):
    labelsDictionary = {}

    if (labels is not None) and (len(labels) > 0):
        labelsDictionary = __parseLabels(labels)

    testRuns = loadJunitTestRuns(body)
    testRunsIds = junitDatabase.insertTestRuns(testRuns, labelsDictionary)

    result = {
        "numberOfItems" : len(testRunsIds),
        "ids" : testRunsIds
    }
    return result, 201

def query(body):
    testRuns = junitDatabase.queryTestRuns(body)
    return marshallTestRuns(testRuns)

def delete(id):
    junitDatabase.deleteTestRun(id)
    
    return id

def health():
    return "Ready!"

def __parseLabels(str):
    labels = {}

    if len(str) == 0:
        return labels

    labelPairs = str.split(",")
    for pair in labelPairs:
        pairSplitted = pair.split(":", 1)
        key = pairSplitted[0]
        value = pairSplitted[1]

        labels[key] = value

    return labels

def marshallTestRuns(data):
    if (type(data).__name__ == "Pagination"):       
        return {
            "page": data.page,
            "per_page": data.per_page,
            "total": data.total,
            "items": list(map(lambda t : t.as_dict(), data.items))
        }
    else:
        return list(map(lambda t : t.as_dict(), data))
