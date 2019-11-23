import json
from junit import loadJunitTestRuns

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

def health():
    return "Ready!"
